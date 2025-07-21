"""
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from enciclopedia.views import enciclopedia_indice, enciclopedia_attacchi, index, rilevamento_attacco, \
    risultati_attacco, genera_report_attacco_pdf
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('admin/', admin.site.urls),
    #path("enciclopedia/", include("enciclopedia.urls")),
    path('', index, name="index"),
    path('enciclopedia_indice', enciclopedia_indice, name='enciclopedia_indice'),
    path('enciclopedia_attacchi/<int:attacco_id>/', enciclopedia_attacchi, name='enciclopedia_attacchi'),
    path('rilevamento', rilevamento_attacco, name='rilevamento_attacco'),
    path('risultati/', risultati_attacco, name='risultati_attacco'),
    path('report-pdf/', genera_report_attacco_pdf, name='genera_report_attacco_pdf'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
