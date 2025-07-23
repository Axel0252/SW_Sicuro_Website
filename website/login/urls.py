from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('checkLogin', checkLogin, name="login"),
    path('registrazione_azienda', registrazione_azienda),
    path('registrazione_privato', registrazione_privato),
]
