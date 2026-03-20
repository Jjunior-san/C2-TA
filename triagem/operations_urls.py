from django.urls import path

from . import operations_views

app_name = 'triagem-ops'

urlpatterns = [
    path('operacional/cidadaos/novo/', operations_views.citizen_create, name='citizen-create'),
    path('operacional/senhas/emitir/', operations_views.issue_ticket, name='issue-ticket'),
    path('painel/', operations_views.panel, name='panel'),
]
