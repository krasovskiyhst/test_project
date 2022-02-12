from django.shortcuts import render
from .models import AccessLogs
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    logs = AccessLogs.objects.all()
    context = {'logs': logs}
    return render(request, 'index.html', context)
