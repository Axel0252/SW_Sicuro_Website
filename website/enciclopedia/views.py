from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from enciclopedia.models import EnciclopediaAttacchi, ConsultazioneAttacco, Attacco


# Create your views here.

def index(request):
    return render(request, 'index.html', {})
    #return HttpResponse("Enciclopedia Test.")

def enciclopedia_indice(request):
    categorie = EnciclopediaAttacchi.objects.all()
    return render(request, 'enciclopedia_indice.html', {'categorie': categorie})

def enciclopedia_attacchi(request, attacco_id):
    attacco = get_object_or_404(Attacco, id=attacco_id)

    # Correggi i \n testuali in veri newline
    attacco.descrizione = attacco.descrizione.replace('\\n', '\n')
    attacco.contromisure = attacco.contromisure.replace('\\n', '\n')

    if request.user.is_authenticated:
        ConsultazioneAttacco.objects.create(
            attacco=attacco,
            utente=request.user,
            ora_consultazione=timezone.now().time()
        )

    return render(request, 'enciclopedia_attacchi.html', {'attacco': attacco})