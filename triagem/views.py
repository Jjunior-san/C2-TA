from django.http import HttpResponse


def home(request):
    return HttpResponse('C2-TA online')
