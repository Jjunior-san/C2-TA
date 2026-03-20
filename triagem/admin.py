from django.contrib import admin

from .citizen_profile import CitizenProfileExtension
from .integration_models import (
    ERPDepartmentMirror,
    ERPOperatorMirror,
    ERPSecretariatMirror,
    IntegrationEventLog,
    OutboundSyncQueue,
)
from .models import AttendanceUnit, CitizenRecord, QueueTicket, ServiceCatalog


@admin.register(AttendanceUnit)
class AttendanceUnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'phone', 'email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code', 'email', 'phone')


@admin.register(ServiceCatalog)
class ServiceCatalogAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'unit', 'estimated_minutes', 'requires_screening', 'is_active')
    list_filter = ('unit', 'requires_screening', 'is_active')
    search_fields = ('name', 'code', 'description')


@admin.register(CitizenRecord)
class CitizenRecordAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'tax_id', 'phone', 'email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('full_name', 'tax_id', 'phone', 'email')


@admin.register(QueueTicket)
class QueueTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'unit', 'service', 'citizen', 'status', 'issued_at')
    list_filter = ('unit', 'service', 'status')
    search_fields = ('ticket_number', 'citizen__full_name', 'citizen__tax_id')


@admin.register(CitizenProfileExtension)
class CitizenProfileExtensionAdmin(admin.ModelAdmin):
    list_display = ('citizen', 'social_name', 'city', 'sync_status', 'last_synced_at')
    list_filter = ('sync_status', 'city')
    search_fields = ('citizen__full_name', 'social_name', 'erp_citizen_id', 'external_reference')


@admin.register(ERPSecretariatMirror)
class ERPSecretariatMirrorAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_active', 'last_synced_at')
    list_filter = ('is_active',)
    search_fields = ('code', 'name')


@admin.register(ERPDepartmentMirror)
class ERPDepartmentMirrorAdmin(admin.ModelAdmin):
    list_display = ('secretariat', 'code', 'name', 'email', 'is_active', 'last_synced_at')
    list_filter = ('secretariat', 'is_active')
    search_fields = ('code', 'name', 'email', 'secretariat_code')


@admin.register(ERPOperatorMirror)
class ERPOperatorMirrorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'employee_number', 'secretariat_code', 'department_code', 'status', 'last_synced_at')
    list_filter = ('status', 'secretariat_code', 'department_code')
    search_fields = ('full_name', 'employee_number', 'tax_id')


@admin.register(OutboundSyncQueue)
class OutboundSyncQueueAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'target_path', 'status', 'attempts', 'external_reference', 'sent_at')
    list_filter = ('status', 'event_type')
    search_fields = ('event_type', 'target_path', 'external_reference')


@admin.register(IntegrationEventLog)
class IntegrationEventLogAdmin(admin.ModelAdmin):
    list_display = ('direction', 'event_type', 'target', 'success', 'external_reference', 'response_status', 'created_at')
    list_filter = ('direction', 'success', 'event_type')
    search_fields = ('event_type', 'target', 'external_reference', 'error_message')
