from django.test import TestCase

from triagem.call_service import CallService, CallServiceError
from triagem.models import AttendanceUnit, QueueTicket, ServiceCatalog
from triagem.services import TicketService, TicketServiceError


class TicketServiceTests(TestCase):
    def setUp(self):
        self.unit = AttendanceUnit.objects.create(name='Central', code='CENTRAL')
        self.service = ServiceCatalog.objects.create(
            unit=self.unit,
            name='Cadastro',
            code='CAD',
            estimated_minutes=10,
            requires_screening=True,
        )

    def test_issue_ticket_generates_daily_sequence(self):
        first = TicketService.issue_ticket(unit_code='CENTRAL', service_code='CAD')
        second = TicketService.issue_ticket(unit_code='CENTRAL', service_code='CAD')

        self.assertEqual(first.daily_sequence, 1)
        self.assertEqual(second.daily_sequence, 2)
        self.assertEqual(first.ticket_number, 'A0001')
        self.assertEqual(second.ticket_number, 'A0002')
        self.assertEqual(first.issued_on, second.issued_on)

    def test_issue_ticket_rejects_unknown_unit(self):
        with self.assertRaises(TicketServiceError):
            TicketService.issue_ticket(unit_code='UNKNOWN', service_code='CAD')


class CallServiceTests(TestCase):
    def setUp(self):
        self.unit = AttendanceUnit.objects.create(name='Central', code='CENTRAL')
        self.service = ServiceCatalog.objects.create(
            unit=self.unit,
            name='Cadastro',
            code='CAD',
            estimated_minutes=10,
            requires_screening=True,
        )

    def test_call_next_updates_ticket_status(self):
        issued = TicketService.issue_ticket(unit_code='CENTRAL', service_code='CAD')

        called = CallService.call_next()
        issued.refresh_from_db()

        self.assertEqual(called.id, issued.id)
        self.assertEqual(issued.status, QueueTicket.Status.CALLED)
        self.assertIsNotNone(issued.called_at)

    def test_call_next_without_waiting_ticket_raises_error(self):
        with self.assertRaises(CallServiceError):
            CallService.call_next()
