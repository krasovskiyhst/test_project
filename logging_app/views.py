from django.shortcuts import render
from .models import AccessLogs
from .forms import DateForm, IPForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import viewsets
from .serializers import AccessLogsSerializer


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


class AccessLogsViewSet(viewsets.ModelViewSet):
    queryset = AccessLogs.objects.all()
    serializer_class = AccessLogsSerializer
    date_from_url_kwarg = 'date_from'
    date_to_url_kwarg = 'date_to'

    def get_queryset(self):
        date_from = self.request.query_params.get(self.date_from_url_kwarg)
        date_to = self.request.query_params.get(self.date_to_url_kwarg)
        if date_from and date_to:
            return AccessLogs.objects.filter(date__range=[date_from, date_to])
        return AccessLogs.objects.all()
