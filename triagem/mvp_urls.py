from django.urls import include, path

from . import operations_views

app_name = 'triagem'

urlpatterns = [
    path('', operations_views.panel, name='home-panel'),
    path('operacional/', include('triagem.operations_urls')),
    path('painel/', operations_views.panel, name='panel'),
]
