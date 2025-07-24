from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', numeri_index, name="numeri_index"),
    path('analisi_numeri', analisi_numeri, name="analisi_numeri"),
]