from django.test import Client, TestCase


class SmokeRoutesTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_route_responds(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_panel_route_responds(self):
        response = self.client.get('/painel/')
        self.assertEqual(response.status_code, 200)

    def test_citizen_create_route_responds(self):
        response = self.client.get('/operacional/cidadaos/novo/')
        self.assertEqual(response.status_code, 200)

    def test_issue_ticket_route_responds(self):
        response = self.client.get('/operacional/senhas/emitir/')
        self.assertEqual(response.status_code, 200)

    def test_call_next_route_responds(self):
        response = self.client.get('/guiche/chamar-proximo/')
        self.assertEqual(response.status_code, 200)
