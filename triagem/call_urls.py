from django.urls import path

from . import call_views

app_name = 'triagem-call'

urlpatterns = [
    path('guiche/chamar-proximo/', call_views.call_next, name='call-next'),
    path('guiche/rechamadas/', call_views.recall_panel, name='recall-panel'),
]
