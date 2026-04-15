from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import LoginForm


def _default_redirect_for_user(user):
    return '/painel/'


def _resolve_next_url(request, user=None):
    next_url = request.POST.get('next') or request.GET.get('next')
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    if user is not None:
        return _default_redirect_for_user(user)
    return None


def home(request):
    if request.user.is_authenticated:
        return redirect(_resolve_next_url(request, request.user) or _default_redirect_for_user(request.user))

    form = LoginForm(request=request, data=request.POST or None)
    next_url = _resolve_next_url(request)

    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect(_resolve_next_url(request, user) or _default_redirect_for_user(user))

    return render(request, 'triagem/home.html', {'form': form, 'next_url': next_url or ''})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')
