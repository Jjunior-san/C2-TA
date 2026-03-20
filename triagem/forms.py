from django import forms

from .models import CitizenRecord


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
