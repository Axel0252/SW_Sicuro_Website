from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', analizzatoreIndex, name="analizzatoreIndex"),
    path('checkMessage', checkMessage, name="checkMessage"),
]