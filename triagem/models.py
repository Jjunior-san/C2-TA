from django.db import models
from django.utils import timezone


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActiveModel(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class AttendanceUnit(TimestampedModel, ActiveModel):
    name = models.CharField(max_length=160)
    code = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=240, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ServiceCatalog(TimestampedModel, ActiveModel):
    unit = models.ForeignKey(AttendanceUnit, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=180)
    code = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    estimated_minutes = models.PositiveIntegerField(default=10)
    requires_screening = models.BooleanField(default=True)

    class Meta:
        ordering = ['unit__name', 'name']
        unique_together = ('unit', 'code')

    def __str__(self):
        return f'{self.unit.name} - {self.name}'


class CitizenRecord(TimestampedModel, ActiveModel):
    full_name = models.CharField(max_length=180)
    tax_id = models.CharField(max_length=18, blank=True, db_index=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=240, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class PriorityProfile(TimestampedModel, ActiveModel):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=20, default='#9f1239')
    sort_order = models.PositiveIntegerField(default=0)
    target_wait_minutes = models.PositiveIntegerField(default=15)
    is_preferential = models.BooleanField(default=False)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class Appointment(TimestampedModel):
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Agendado'
        CONFIRMED = 'confirmed', 'Confirmado'
        CHECKED_IN = 'checked_in', 'Recepcionado'
        COMPLETED = 'completed', 'Concluído'
        CANCELLED = 'cancelled', 'Cancelado'

    unit = models.ForeignKey(AttendanceUnit, on_delete=models.PROTECT, related_name='appointments')
    service = models.ForeignKey(ServiceCatalog, on_delete=models.PROTECT, related_name='appointments')
    citizen = models.ForeignKey(CitizenRecord, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    priority_profile = models.ForeignKey(
        PriorityProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments',
    )
    citizen_name = models.CharField(max_length=180, blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    scheduled_for = models.DateTimeField(db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['scheduled_for', 'created_at']
        indexes = [
            models.Index(fields=['unit', 'status', 'scheduled_for']),
        ]

    def __str__(self):
        return self.citizen_name or (self.citizen.full_name if self.citizen else f'Agendamento {self.pk}')


class QueueTicket(TimestampedModel):
    class Status(models.TextChoices):
        ISSUED = 'issued', 'Emitida'
        SCREENING = 'screening', 'Em triagem'
        WAITING = 'waiting', 'Aguardando'
        CALLED = 'called', 'Chamada'
        IN_SERVICE = 'in_service', 'Em atendimento'
        FINISHED = 'finished', 'Finalizada'
        CANCELLED = 'cancelled', 'Cancelada'

    unit = models.ForeignKey(AttendanceUnit, on_delete=models.PROTECT, related_name='tickets')
    service = models.ForeignKey(ServiceCatalog, on_delete=models.PROTECT, related_name='tickets')
    citizen = models.ForeignKey(CitizenRecord, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
    ticket_number = models.CharField(max_length=20, db_index=True)
    issued_on = models.DateField(default=timezone.localdate, db_index=True)
    daily_sequence = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ISSUED)
    issued_at = models.DateTimeField(default=timezone.now)
    waiting_started_at = models.DateTimeField(null=True, blank=True)
    called_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-issued_at']
        constraints = [
            models.UniqueConstraint(
                fields=['unit', 'issued_on', 'daily_sequence'],
                name='uq_queue_ticket_unit_day_sequence',
            ),
            models.UniqueConstraint(
                fields=['unit', 'issued_on', 'ticket_number'],
                name='uq_queue_ticket_unit_day_number',
            ),
        ]
        indexes = [
            models.Index(fields=['unit', 'status', 'issued_on', 'issued_at']),
            models.Index(fields=['ticket_number']),
        ]

    def __str__(self):
        return self.ticket_number


from .citizen_profile import CitizenProfileExtension  # noqa: E402,F401
from .integration_models import (  # noqa: E402,F401
    ERPDepartmentMirror,
    ERPOperatorMirror,
    ERPSecretariatMirror,
    IntegrationEventLog,
    OutboundSyncQueue,
)
