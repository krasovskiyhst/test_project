from django.shortcuts import render
from .models import AccessLogs
from .forms import DateForm, IPForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required
def index(request):
    date_form = DateForm(request.POST or None)
    ip_form = IPForm(request.POST or None)
    logs = AccessLogs.objects.all()
    context = {'logs': logs, 'date_form': date_form, 'ip_form': ip_form}
    if request.method == 'POST':
        if request.POST.get('date_from') and request.POST.get('date_to') and date_form.is_valid():
            date_from = request.POST.get('date_from')
            date_to = request.POST.get('date_to')
            logs = AccessLogs.objects.filter(date__range=[date_from, date_to])
            context = {'logs': logs, 'date_form': date_form, 'ip_form': ip_form}

        elif request.POST.get('ip') and ip_form.is_valid():
            ip = request.POST.get('ip')
            logs = AccessLogs.objects.filter(ip=ip)
            context = {'logs': logs, 'date_form': date_form, 'ip_form': ip_form}

    return render(request, 'index.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
