from django.urls import path, re_path
from .views import AddcommentView
# from django.views.decorators.csrf import csrf_exempt
# from .views import *

app_name = 'comment'
urlpatterns = [
    re_path(r'^add/$', AddcommentView, name='add_comment'),
]


