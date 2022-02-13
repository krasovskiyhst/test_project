from django.urls import path
from . import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', views.index, name='home'),
    path('login/', LoginView.as_view(template_name='login.html'), name="login"),
    path('logout', views.logout_view, name='logout'),
]
