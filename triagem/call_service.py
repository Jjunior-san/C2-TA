from django.db import transaction
from django.utils import timezone

from .models import QueueTicket


class CallServiceError(Exception):
    pass


class CallService:
    @staticmethod
    def next_waiting_ticket():
        return (
            QueueTicket.objects.select_for_update()
            .filter(status=QueueTicket.Status.ISSUED)
            .order_by('issued_at', 'id')
            .first()
        )

    @classmethod
    def call_next(cls):
        with transaction.atomic():
            ticket = cls.next_waiting_ticket()
            if not ticket:
                raise CallServiceError('Nenhuma senha aguardando para chamada.')

            ticket.status = QueueTicket.Status.CALLED
            ticket.called_at = timezone.now()
            ticket.save(update_fields=['status', 'called_at', 'updated_at'])
            return ticket
