from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from triagem.models import AttendanceUnit, ServiceCatalog


class SmokeRoutesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='operador',
            password='senha-segura-123',
            is_staff=True,
        )
        self.unit = AttendanceUnit.objects.create(name='Central', code='CENTRAL')
        self.service = ServiceCatalog.objects.create(
            unit=self.unit,
            name='Cadastro',
            code='CAD',
            estimated_minutes=10,
            requires_screening=True,
        )

    def login(self):
        self.client.force_login(self.user)

    def test_home_route_responds(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_login_authenticates_and_redirects(self):
        response = self.client.post(
            '/',
            {
                'username': 'operador',
                'password': 'senha-segura-123',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/painel/')

    def test_panel_route_responds(self):
        self.login()
        response = self.client.get('/painel/')
        self.assertEqual(response.status_code, 200)

    def test_monitor_route_responds(self):
        self.login()
        response = self.client.get('/monitor/')
        self.assertEqual(response.status_code, 200)

    def test_internal_routes_require_login(self):
        response = self.client.get('/painel/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/?next=/painel/', response['Location'])

    def test_citizen_create_route_responds(self):
        self.login()
        response = self.client.get('/operacional/cidadaos/novo/')
        self.assertEqual(response.status_code, 200)

    def test_issue_ticket_route_responds(self):
        self.login()
        response = self.client.get('/operacional/senhas/emitir/')
        self.assertEqual(response.status_code, 200)

    def test_call_next_route_responds(self):
        self.login()
        response = self.client.get('/guiche/chamar-proximo/')
        self.assertEqual(response.status_code, 200)

    def test_schedule_route_creates_appointment(self):
        self.login()
        response = self.client.post(
            '/agendamento/',
            {
                'citizen_name': 'Maria de Teste',
                'unit': self.unit.id,
                'service': self.service.id,
                'scheduled_for': '2026-04-15T10:30',
                'contact_phone': '75999999999',
                'notes': 'Retorno agendado.',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/agendamento/')

    def test_priorities_route_creates_priority(self):
        self.login()
        response = self.client.post(
            '/prioridades/',
            {
                'name': 'Preferencial',
                'code': 'PREF',
                'description': 'Fila preferencial',
                'color': '#9f1239',
                'sort_order': 1,
                'target_wait_minutes': 10,
                'is_preferential': 'on',
                'is_active': 'on',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/prioridades/')
