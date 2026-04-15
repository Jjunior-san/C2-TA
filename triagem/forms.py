from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone

from .models import Appointment, AttendanceUnit, CitizenRecord, PriorityProfile, ServiceCatalog


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Nome de usuário',
                'autocomplete': 'username',
                'autofocus': True,
            }
        ),
    )
    password = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Senha',
                'autocomplete': 'current-password',
            }
        ),
    )


class CitizenRecordForm(forms.ModelForm):
    class Meta:
        model = CitizenRecord
        fields = [
            'full_name',
            'tax_id',
            'birth_date',
            'phone',
            'email',
            'address',
            'notes',
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class IssueTicketForm(forms.Form):
    citizen = forms.ModelChoiceField(
        queryset=CitizenRecord.objects.filter(is_active=True).order_by('full_name'),
        required=False,
        empty_label='Selecione um cidadão cadastrado',
    )
    citizen_name = forms.CharField(max_length=180, required=False)
    service_code = forms.CharField(max_length=30)
    unit_code = forms.CharField(max_length=30)
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))


class AppointmentForm(forms.Form):
    citizen = forms.ModelChoiceField(
        queryset=CitizenRecord.objects.filter(is_active=True).order_by('full_name'),
        required=False,
        empty_label='Selecione um cidadão cadastrado',
    )
    citizen_name = forms.CharField(max_length=180, required=False)
    unit = forms.ModelChoiceField(
        queryset=AttendanceUnit.objects.filter(is_active=True).order_by('name'),
    )
    service = forms.ModelChoiceField(
        queryset=ServiceCatalog.objects.filter(is_active=True).select_related('unit').order_by('unit__name', 'name'),
    )
    priority_profile = forms.ModelChoiceField(
        queryset=PriorityProfile.objects.filter(is_active=True).order_by('sort_order', 'name'),
        required=False,
        empty_label='Sem prioridade específica',
    )
    scheduled_for = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    )
    contact_phone = forms.CharField(max_length=30, required=False)
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['scheduled_for'].initial = timezone.localtime().replace(second=0, microsecond=0).strftime('%Y-%m-%dT%H:%M')

    def clean(self):
        cleaned_data = super().clean()
        citizen = cleaned_data.get('citizen')
        citizen_name = (cleaned_data.get('citizen_name') or '').strip()
        unit = cleaned_data.get('unit')
        service = cleaned_data.get('service')

        if not citizen and not citizen_name:
            self.add_error('citizen_name', 'Informe o nome do cidadão quando não houver cadastro selecionado.')

        if unit and service and service.unit_id != unit.id:
            self.add_error('service', 'O serviço selecionado não pertence à unidade informada.')

        return cleaned_data


class PriorityProfileForm(forms.ModelForm):
    class Meta:
        model = PriorityProfile
        fields = [
            'name',
            'code',
            'description',
            'color',
            'sort_order',
            'target_wait_minutes',
            'is_preferential',
            'is_active',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'color': forms.TextInput(attrs={'type': 'color'}),
        }
