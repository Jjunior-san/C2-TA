from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render

from .forms import AppointmentForm, CitizenRecordForm, IssueTicketForm, PriorityProfileForm
from .models import Appointment, AttendanceUnit, CitizenRecord, PriorityProfile, QueueTicket, ServiceCatalog
from .services import TicketService, TicketServiceError


MAIN_MODULES = [
    {'label': 'Agendamento', 'badge': 'AG', 'url': '/agendamento/'},
    {'label': 'Atendimento', 'badge': 'AT', 'url': '/guiche/chamar-proximo/'},
    {'label': 'Cidadãos', 'badge': 'CI', 'url': '/operacional/cidadaos/novo/'},
    {'label': 'Configurações', 'badge': 'CF', 'url': '/admin/'},
    {'label': 'Monitor', 'badge': 'MN', 'url': '/monitor/'},
    {'label': 'Relatórios', 'badge': 'RL', 'url': '/relatorios/'},
    {'label': 'Triagem', 'badge': 'TR', 'url': '/operacional/senhas/emitir/'},
    {'label': 'Usuários', 'badge': 'US', 'url': '/admin/auth/user/'},
]

ADMIN_MODULES = [
    {'label': 'Sistema', 'badge': 'SI', 'url': '/admin/'},
    {'label': 'Serviços', 'badge': 'SV', 'url': '/admin/triagem/servicecatalog/'},
    {'label': 'Perfis', 'badge': 'PF', 'url': '/admin/auth/group/'},
    {'label': 'Prioridades', 'badge': 'PR', 'url': '/prioridades/'},
    {'label': 'Locais', 'badge': 'LC', 'url': '/admin/triagem/attendanceunit/'},
]

MODULE_PAGES = {
    'suporte': {
        'title': 'Suporte',
        'eyebrow': 'Ajuda',
        'description': 'Canal institucional do C² para apoio operacional e evolução do ambiente.',
    },
}


def _display_name(request):
    if request.user.is_authenticated:
        return request.user.get_short_name() or request.user.get_username()
    return 'Operador'


@login_required(login_url='/')
def dashboard(request):
    return render(
        request,
        'triagem/dashboard.html',
        {
            'display_name': _display_name(request),
            'main_modules': MAIN_MODULES,
            'admin_modules': ADMIN_MODULES,
        },
    )


@login_required(login_url='/')
def schedule_page(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            citizen = form.cleaned_data.get('citizen')
            citizen_name = (form.cleaned_data.get('citizen_name') or '').strip()
            contact_phone = form.cleaned_data.get('contact_phone', '')

            if not citizen and citizen_name:
                citizen = CitizenRecord.objects.create(full_name=citizen_name, phone=contact_phone)

            appointment = Appointment.objects.create(
                citizen=citizen,
                citizen_name=citizen.full_name if citizen else citizen_name,
                unit=form.cleaned_data['unit'],
                service=form.cleaned_data['service'],
                priority_profile=form.cleaned_data.get('priority_profile'),
                scheduled_for=form.cleaned_data['scheduled_for'],
                contact_phone=contact_phone or (citizen.phone if citizen else ''),
                notes=form.cleaned_data.get('notes', ''),
            )
            messages.success(request, f'Agendamento registrado para {appointment.citizen_name}.')
            return redirect('/agendamento/')
    else:
        form = AppointmentForm()

    upcoming_appointments = Appointment.objects.select_related(
        'citizen', 'unit', 'service', 'priority_profile'
    ).order_by('scheduled_for')[:12]
    return render(
        request,
        'triagem/schedule.html',
        {
            'form': form,
            'upcoming_appointments': upcoming_appointments,
        },
    )


@login_required(login_url='/')
def citizen_create(request):
    if request.method == 'POST':
        form = CitizenRecordForm(request.POST)
        if form.is_valid():
            citizen = form.save()
            messages.success(request, f'Cidadão cadastrado: {citizen.full_name}')
            return redirect('/operacional/cidadaos/novo/')
    else:
        form = CitizenRecordForm()
    return render(request, 'triagem/citizen_create.html', {'form': form})


@login_required(login_url='/')
def issue_ticket(request):
    issued_ticket = None
    if request.method == 'POST':
        form = IssueTicketForm(request.POST)
        if form.is_valid():
            try:
                issued_ticket = TicketService.issue_ticket(
                    unit_code=form.cleaned_data['unit_code'],
                    service_code=form.cleaned_data['service_code'],
                    citizen=form.cleaned_data.get('citizen'),
                    citizen_name=form.cleaned_data.get('citizen_name', ''),
                    notes=form.cleaned_data.get('notes', ''),
                )
                messages.success(request, f'Senha emitida com sucesso: {issued_ticket.ticket_number}')
            except TicketServiceError as exc:
                messages.error(request, str(exc))
    else:
        form = IssueTicketForm()
    return render(request, 'triagem/issue_ticket.html', {'form': form, 'issued_ticket': issued_ticket})


@login_required(login_url='/')
def priorities_page(request):
    if request.method == 'POST':
        form = PriorityProfileForm(request.POST)
        if form.is_valid():
            priority = form.save()
            messages.success(request, f'Prioridade cadastrada: {priority.name}')
            return redirect('/prioridades/')
    else:
        form = PriorityProfileForm()

    priorities = PriorityProfile.objects.order_by('sort_order', 'name')
    return render(
        request,
        'triagem/priorities.html',
        {
            'form': form,
            'priorities': priorities,
        },
    )


@login_required(login_url='/')
def monitor(request):
    waiting = QueueTicket.objects.filter(status=QueueTicket.Status.ISSUED).order_by('issued_at')[:20]
    called = QueueTicket.objects.filter(status=QueueTicket.Status.CALLED).order_by('-called_at')[:10]
    return render(request, 'triagem/panel.html', {'waiting': waiting, 'called': called})


@login_required(login_url='/')
def reports(request):
    metrics = [
        {'label': 'Senhas emitidas', 'value': QueueTicket.objects.count()},
        {'label': 'Cidadãos cadastrados', 'value': CitizenRecord.objects.count()},
        {'label': 'Serviços ativos', 'value': ServiceCatalog.objects.filter(is_active=True).count()},
        {'label': 'Locais ativos', 'value': AttendanceUnit.objects.filter(is_active=True).count()},
        {'label': 'Agendamentos', 'value': Appointment.objects.count()},
        {'label': 'Prioridades', 'value': PriorityProfile.objects.count()},
    ]
    return render(
        request,
        'triagem/module_page.html',
        {
            'title': 'Relatórios',
            'eyebrow': 'Operação',
            'description': 'Resumo operacional do ambiente atual do C2-TA.',
            'metrics': metrics,
        },
    )


@login_required(login_url='/')
def module_page(request, slug):
    module = MODULE_PAGES.get(slug)
    if not module:
        raise Http404('Módulo não encontrado.')
    return render(request, 'triagem/module_page.html', module)
