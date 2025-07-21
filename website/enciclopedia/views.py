from django.http import HttpResponse
from django.utils import timezone
import re
from django.utils.html import escape, mark_safe
from django.shortcuts import render, redirect, get_object_or_404
from enciclopedia.models import EnciclopediaAttacchi, ConsultazioneAttacco, Attacco



# Create your views here.

def index(request):
    return render(request, 'index.html', {})
    #return HttpResponse("Enciclopedia Test.")

def enciclopedia_indice(request):
    categorie = EnciclopediaAttacchi.objects.all()
    return render(request, 'enciclopedia_indice.html', {'categorie': categorie})

import re
from django.utils.html import escape, mark_safe

def enciclopedia_attacchi(request, attacco_id):
    attacco = get_object_or_404(Attacco, id=attacco_id)

    def formatta_testo(testo):
        # Pulisce newline e backslash
        testo = testo.replace('\\n', '\n').replace('\\', '')

        # Escape del testo per evitare XSS
        from django.utils.html import escape, mark_safe
        testo = escape(testo)

        # Evidenzia titoli (senza lookbehind)
        titoli = [
            "Modalità di esecuzione:",
            "Possibili conseguenze:",
            "Consigli pratici per la prevenzione:"
        ]

        for titolo in titoli:
            # Sostituisce il titolo con la versione in <strong>
            testo = testo.replace(titolo, f"<strong>{titolo}</strong>")

        return mark_safe(testo)

    attacco.descrizione = formatta_testo(attacco.descrizione)
    attacco.contromisure = formatta_testo(attacco.contromisure)

    if request.user.is_authenticated:
        ConsultazioneAttacco.objects.create(
            attacco=attacco,
            utente=request.user,
            ora_consultazione=timezone.now().time()
        )

    return render(request, 'enciclopedia_attacchi.html', {'attacco': attacco})
