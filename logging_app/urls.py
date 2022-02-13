from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from .views import AccessLogsViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('api/v1/access-logs', AccessLogsViewSet, basename='access-logs')
urlpatterns = router.urls

urlpatterns += [
    path('', views.index, name='home'),
    path('login/', LoginView.as_view(template_name='login.html'), name="login"),
    path('logout', views.logout_view, name='logout'),
]
