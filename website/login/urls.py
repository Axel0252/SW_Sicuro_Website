from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', index, name="loginIndex"),
    path('checkLogin', checkLogin, name="login"),
    path('registrazione_azienda', registrazione_azienda),
    path('registrazione_privato', registrazione_privato),
    path('logout', logoutUser, name="logoutUser"),
    path('render_homepage', render_homepage, name="render_homepage")
]
