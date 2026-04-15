from django.urls import include, path

from . import views

app_name = 'triagem'

urlpatterns = [
    path('', views.home, name='home'),
    path('sair/', views.logout_view, name='logout'),
    path('', include('triagem.operations_urls')),
    path('', include('triagem.call_urls')),
]
