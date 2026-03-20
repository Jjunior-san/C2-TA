from django.db import models

from .models import ActiveModel, TimestampedModel


class ERPSecretariatMirror(TimestampedModel, ActiveModel):
    erp_id = models.PositiveIntegerField(unique=True)
    code = models.CharField(max_length=20, db_index=True)
    name = models.CharField(max_length=180)
    raw_payload = models.JSONField(default=dict, blank=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.code} - {self.name}'


class ERPDepartmentMirror(TimestampedModel, ActiveModel):
    erp_id = models.PositiveIntegerField(unique=True)
    secretariat = models.ForeignKey(
        ERPSecretariatMirror,
        on_delete=models.CASCADE,
        related_name='departments',
    )
    secretariat_code = models.CharField(max_length=20, blank=True)
    code = models.CharField(max_length=20, db_index=True)
    name = models.CharField(max_length=180)
    email = models.EmailField(blank=True)
    raw_payload = models.JSONField(default=dict, blank=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['secretariat__name', 'name']

    def __str__(self):
        return f'{self.secretariat.code} - {self.name}'


class ERPOperatorMirror(TimestampedModel, ActiveModel):
    erp_employee_id = models.PositiveIntegerField(unique=True)
    erp_user_id = models.PositiveIntegerField(null=True, blank=True)
    full_name = models.CharField(max_length=180)
    employee_number = models.CharField(max_length=40, blank=True)
    tax_id = models.CharField(max_length=18, blank=True)
    secretariat_code = models.CharField(max_length=20, blank=True)
    department_code = models.CharField(max_length=20, blank=True)
    position_title = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=20, default='active')
    raw_payload = models.JSONField(default=dict, blank=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class OutboundSyncQueue(TimestampedModel):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendente'
        SENT = 'sent', 'Enviado'
        FAILED = 'failed', 'Falhou'

    event_type = models.CharField(max_length=80)
    target_path = models.CharField(max_length=200)
    payload = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    attempts = models.PositiveIntegerField(default=0)
    external_reference = models.CharField(max_length=80, blank=True, db_index=True)
    last_error = models.TextField(blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.event_type} - {self.status}'


class IntegrationEventLog(TimestampedModel):
    class Direction(models.TextChoices):
        OUTBOUND = 'outbound', 'Saída'
        INBOUND = 'inbound', 'Entrada'

    direction = models.CharField(max_length=20, choices=Direction.choices, default=Direction.OUTBOUND)
    event_type = models.CharField(max_length=80)
    target = models.CharField(max_length=200, blank=True)
    success = models.BooleanField(default=False)
    external_reference = models.CharField(max_length=80, blank=True, db_index=True)
    request_payload = models.JSONField(default=dict, blank=True)
    response_payload = models.JSONField(default=dict, blank=True)
    response_status = models.PositiveIntegerField(null=True, blank=True)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.direction} - {self.event_type}'
