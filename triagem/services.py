from django.utils import timezone

from .models import AttendanceUnit, CitizenRecord, QueueTicket, ServiceCatalog


class TicketServiceError(Exception):
    pass


class TicketService:
    @staticmethod
    def next_sequence(unit):
        today = timezone.localdate()
        count = QueueTicket.objects.filter(unit=unit, issued_at__date=today).count()
        return count + 1

    @staticmethod
    def build_ticket_number(sequence):
        return f"A{sequence:04d}"

    @classmethod
    def issue_ticket(cls, *, unit_code, service_code, citizen=None, citizen_name='', notes=''):
        try:
            unit = AttendanceUnit.objects.get(code=unit_code, is_active=True)
        except AttendanceUnit.DoesNotExist as exc:
            raise TicketServiceError('Unidade não encontrada.') from exc

        try:
            service = ServiceCatalog.objects.get(unit=unit, code=service_code, is_active=True)
        except ServiceCatalog.DoesNotExist as exc:
            raise TicketServiceError('Serviço não encontrado para a unidade.') from exc

        local_citizen = citizen
        if not local_citizen and citizen_name:
            local_citizen = CitizenRecord.objects.create(full_name=citizen_name.strip())

        sequence = cls.next_sequence(unit)
        ticket_number = cls.build_ticket_number(sequence)

        return QueueTicket.objects.create(
            unit=unit,
            service=service,
            citizen=local_citizen,
            ticket_number=ticket_number,
            daily_sequence=sequence,
            status=QueueTicket.Status.ISSUED,
            waiting_started_at=timezone.now(),
            notes=notes or '',
        )
