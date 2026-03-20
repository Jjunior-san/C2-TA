from django.contrib import messages
from django.shortcuts import redirect, render

from .call_service import CallService, CallServiceError
from .models import QueueTicket


def call_next(request):
    called_ticket = None
    if request.method == 'POST':
        try:
            called_ticket = CallService.call_next()
            messages.success(request, f'Senha chamada: {called_ticket.ticket_number}')
        except CallServiceError as exc:
            messages.warning(request, str(exc))

    waiting = QueueTicket.objects.filter(status=QueueTicket.Status.ISSUED).order_by('issued_at')[:20]
    called = QueueTicket.objects.filter(status=QueueTicket.Status.CALLED).order_by('-called_at')[:10]
    return render(
        request,
        'triagem/call_next.html',
        {
            'waiting': waiting,
            'called': called,
            'called_ticket': called_ticket,
        },
    )


def recall_panel(request):
    called = QueueTicket.objects.filter(status=QueueTicket.Status.CALLED).order_by('-called_at')[:10]
    return render(request, 'triagem/recall_panel.html', {'called': called})
