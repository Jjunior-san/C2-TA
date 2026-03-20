from django.contrib import admin

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
