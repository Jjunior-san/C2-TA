import os

import requests


class ERPClientError(Exception):
    pass


class ERPClient:
    def __init__(self):
        self.base_url = os.environ.get('C2TA_ERP_BASE_URL', '').rstrip('/')
        self.token = os.environ.get('C2TA_ERP_API_TOKEN', '')
        self.timeout = int(os.environ.get('C2TA_ERP_TIMEOUT_SECONDS', '20'))
        self.verify_ssl = os.environ.get('C2TA_ERP_VERIFY_SSL', '1') == '1'

    @property
    def headers(self):
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers

    def _url(self, path):
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path, params=None):
        if not self.base_url:
            raise ERPClientError('C2TA_ERP_BASE_URL não configurada.')
        response = requests.get(
            self._url(path),
            headers=self.headers,
            params=params or {},
            timeout=self.timeout,
            verify=self.verify_ssl,
        )
        if not response.ok:
            raise ERPClientError(f'Falha na consulta ao ERP: {response.status_code} {response.text}')
        return response.json()

    def post(self, path, payload=None):
        if not self.base_url:
            raise ERPClientError('C2TA_ERP_BASE_URL não configurada.')
        response = requests.post(
            self._url(path),
            headers=self.headers,
            json=payload or {},
            timeout=self.timeout,
            verify=self.verify_ssl,
        )
        if not response.ok:
            raise ERPClientError(f'Falha no envio ao ERP: {response.status_code} {response.text}')
        return response.json()
