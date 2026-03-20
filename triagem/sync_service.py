from django.utils import timezone

from .erp_client import ERPClient, ERPClientError


class ERPSyncService:
    def __init__(self):
        self.client = ERPClient()

    def fetch_secretariats(self):
        return self.client.get('/api/integration/secretariats/')

    def fetch_departments(self, secretariat_code=None):
        params = {}
        if secretariat_code:
            params['secretariat_code'] = secretariat_code
        return self.client.get('/api/integration/departments/', params=params)

    def fetch_employees(self, department_code=None):
        params = {}
        if department_code:
            params['department_code'] = department_code
        return self.client.get('/api/integration/employees/', params=params)

    def send_attendance_event(self, payload):
        payload = payload or {}
        payload.setdefault('sent_at', timezone.now().isoformat())
        return self.client.post('/api/integration/attendance-events/', payload=payload)

    def create_support_ticket(self, payload):
        return self.client.post('/api/integration/support-tickets/', payload=payload or {})

    def create_calendar_event(self, payload):
        return self.client.post('/api/integration/calendar-events/', payload=payload or {})


def healthcheck_erp():
    try:
        client = ERPClient()
        client.get('/api/integration/secretariats/')
        return {'ok': True}
    except ERPClientError as exc:
        return {'ok': False, 'error': str(exc)}
