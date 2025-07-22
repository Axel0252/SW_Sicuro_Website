from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('checkLogin', checkLogin, name="login"),
    path('scelta_privato', scelta_privato, name="scelta_privato"),
    path('scelta_azienda', scelta_azienda, name="scelta_azienda"),
    path('registrazione_azienda', registrazione_azienda),
    path('registrazione_privato', registrazione_privato),
]
