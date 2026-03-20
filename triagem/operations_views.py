from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import CitizenRecordForm, IssueTicketForm
from .models import QueueTicket
from .services import TicketService, TicketServiceError


def citizen_create(request):
    if request.method == 'POST':
        form = CitizenRecordForm(request.POST)
        if form.is_valid():
            citizen = form.save()
            messages.success(request, f'Cidadão cadastrado: {citizen.full_name}')
            return redirect('triagem-ops:citizen-create')
    else:
        form = CitizenRecordForm()
    return render(request, 'triagem/citizen_create.html', {'form': form})


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


def panel(request):
    waiting = QueueTicket.objects.filter(status=QueueTicket.Status.ISSUED).order_by('issued_at')[:20]
    called = QueueTicket.objects.filter(status=QueueTicket.Status.CALLED).order_by('-called_at')[:10]
    return render(request, 'triagem/panel.html', {'waiting': waiting, 'called': called})
