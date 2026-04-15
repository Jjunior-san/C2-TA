from django.urls import path

from . import operations_views

app_name = 'triagem-ops'

urlpatterns = [
    path('agendamento/', operations_views.schedule_page, name='schedule'),
    path('operacional/cidadaos/novo/', operations_views.citizen_create, name='citizen-create'),
    path('operacional/senhas/emitir/', operations_views.issue_ticket, name='issue-ticket'),
    path('painel/', operations_views.dashboard, name='panel'),
    path('monitor/', operations_views.monitor, name='monitor'),
    path('prioridades/', operations_views.priorities_page, name='priorities'),
    path('relatorios/', operations_views.reports, name='reports'),
    path('modulos/<slug:slug>/', operations_views.module_page, name='module-page'),
]
