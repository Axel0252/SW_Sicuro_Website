from django.urls import path

from . import views
from login.views import *

urlpatterns = [
    path('', index, name="index"),
    path('checkLogin', checkLogin, name="checkLogin"),
]
