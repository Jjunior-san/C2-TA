from django.urls import include, path

from . import operations_views

app_name = 'triagem'

urlpatterns = [
    path('', operations_views.panel, name='home-panel'),
    path('', include('triagem.operations_urls')),
    path('', include('triagem.call_urls')),
    path('painel/', operations_views.panel, name='panel'),
]
