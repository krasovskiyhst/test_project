from django.shortcuts import render
from .tasks import parsing_logs


# @login_required
def index(request):
    parsing_logs()
    return render(request, 'index.html')
