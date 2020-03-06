from django.urls import path, re_path
from . import views
from django.conf import settings
# from django.views.decorators.csrf import csrf_exempt
# from .views import *


app_name = 'account'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name = 'register'),
    path('logout/', views.logout_view, name = 'logout'),
]