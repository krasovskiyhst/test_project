from django.shortcuts import render


# @login_required
def index(request):

    return render(request, 'index.html')
