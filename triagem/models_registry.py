"""Registro central dos modelos do C2-TA.

Este arquivo serve como mapa de consolidação do núcleo do app para a etapa final.
"""

from .citizen_profile import CitizenProfileExtension
from .integration_models import (
    ERPDepartmentMirror,
    ERPOperatorMirror,
    ERPSecretariatMirror,
    IntegrationEventLog,
    OutboundSyncQueue,
)
from .models import AttendanceUnit, CitizenRecord, QueueTicket, ServiceCatalog

__all__ = [
    'AttendanceUnit',
    'CitizenRecord',
    'CitizenProfileExtension',
    'ServiceCatalog',
    'QueueTicket',
    'ERPSecretariatMirror',
    'ERPDepartmentMirror',
    'ERPOperatorMirror',
    'OutboundSyncQueue',
    'IntegrationEventLog',
]
