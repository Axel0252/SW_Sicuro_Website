from django.http import HttpResponse
from django.http.response import FileResponse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.decorators.http import require_http_methods

from enciclopedia.models import EnciclopediaAttacchi, ConsultazioneAttacco, Attacco, RilevamentoAttacco
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
import io
import os
from django.http import FileResponse
from datetime import datetime
from django.conf import settings
import re
from django.utils.html import escape, mark_safe



# Create your views here.

def index(request):
    return render(request, 'index.html', {})
    #return HttpResponse("Enciclopedia Test.")

def enciclopedia_indice(request):
    categorie = EnciclopediaAttacchi.objects.all()
    return render(request, 'enciclopedia_indice.html', {'categorie': categorie})

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


@require_http_methods(["GET", "POST"])
def rilevamento_attacco(request):
    attacchi = RilevamentoAttacco.objects.all()
    tutte_domande = []
    for attacco in attacchi:
        domande = attacco.domande.strip().split('\n')
        for domanda in domande:
            tutte_domande.append((attacco.id, domanda.strip()))

    if request.method == "POST":
        risposte = []
        error = False
        error_msg = None

        for i in range(len(tutte_domande)):
            risposta = request.POST.get(f"domanda_{i}")
            if risposta not in ["sì", "no", "non so"]:
                error = True
                error_msg = "Per favore, rispondi a tutte le domande."
                break
            risposte.append(risposta)

        if error:
            context = {
                "domande": [d[1] for d in tutte_domande],
                "error_msg": error_msg,
                "risposte": risposte,
            }
            return render(request, "rilevamento_attacco.html", context)

        # Analizziamo le risposte per attacco
        risultati = {}
        for i, (attacco_id, domanda) in enumerate(tutte_domande):
            if attacco_id not in risultati:
                risultati[attacco_id] = []
            risultati[attacco_id].append(risposte[i])

        esiti = []
        for attacco in attacchi:
            risposte_attacco = risultati.get(attacco.id, [])
            num_si = risposte_attacco.count("sì")
            if num_si >= 2:
                esiti.append({
                    "titolo": attacco.titolo,
                    "esito": f"Possibile attacco di tipo '{attacco.titolo}' rilevato!",
                    "categoria": attacco.categoria,
                    "domande": attacco.domande.strip().split('\n')
                })
        # se non troviamo nessun attacco sospetto
        if not esiti:
            esiti.append({
                "titolo": "Nessun attacco rilevato",
                "esito": "Non sono stati rilevati attacchi in base alle risposte fornite.",
                "categoria": "",
                "domande": []
            })
        # Salva i risultati in sessione per recuperarli nella pagina risultati
        request.session['esiti'] = esiti

        # Redirect alla pagina dei risultati
        return redirect(reverse('risultati_attacco'))

    else:
        context = {
            "domande": [d[1] for d in tutte_domande],
        }
        return render(request, "rilevamento_attacco.html", context)



def risultati_attacco(request):
    esiti = request.session.get('esiti', None)
    if not esiti:
        return redirect('rilevamento_attacco')

    # Prendi solo gli attacchi con esito positivo
    titoli_attacchi = [e['titolo'] for e in esiti if e['titolo'] != "Nessun attacco rilevato"]

    attacchi_dettagli = Attacco.objects.filter(nome_attacco__in=titoli_attacchi)

    context = {
        "esiti": esiti,
        "attacchi_dettagli": attacchi_dettagli
    }
    return render(request, "risultati_attacco.html", context)


def genera_report_attacco_pdf(request):
    esiti = request.session.get('esiti', [])

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    logo_path = os.path.join(settings.BASE_DIR, 'website', 'static', 'img', 'logo2.png')
    c.drawImage(logo_path, 40, height - 100, width=160, height=80, mask='auto')
    data_ora = datetime.now().strftime("%d/%m/%Y %H:%M")
    c.setFont("Helvetica", 10)
    c.drawRightString(width - 40, height - 40, f"Data e Ora generazione: {data_ora}")

    c.setFont("Helvetica-Bold", 16)
    y = height - 120
    c.drawString(40, y, "Report Risultati Rilevamento Attacco")
    y -= 40

    c.setFont("Helvetica", 12)
    if not esiti:
        c.drawString(40, y, "Nessun risultato disponibile.")
    else:
        for risultato in esiti:
            titolo = risultato.get("titolo", "")
            esito = risultato.get("esito", "")
            categoria = risultato.get("categoria", "")
            domande = risultato.get("domande", [])

            c.setFont("Helvetica-Bold", 14)
            c.drawString(40, y, f"Attacco: {titolo} ({categoria})")
            y -= 20

            c.setFont("Helvetica", 12)
            c.drawString(40, y, f"Esito: {esito}")
            y -= 20

            try:
                attacco_obj = Attacco.objects.get(nome_attacco=titolo)

                # Correggi i \n testuali in veri newline
                descrizione = attacco_obj.descrizione.replace('\\n', '\n')
                contromisure = attacco_obj.contromisure.replace('\\n', '\n')
                livello = attacco_obj.livello_rischio

                c.setFont("Helvetica-Bold", 12)
                c.drawString(40, y, "Descrizione:")
                y -= 15
                c.setFont("Helvetica", 11)
                lines = simpleSplit(descrizione, "Helvetica", 11, width - 80)
                for line in lines:
                    c.drawString(50, y, line)
                    y -= 14
                    if y < 60:
                        c.showPage()
                        y = height - 100

                c.setFont("Helvetica-Bold", 12)
                c.drawString(40, y, "Contromisure:")
                y -= 15
                c.setFont("Helvetica", 11)
                cont_lines = simpleSplit(contromisure, "Helvetica", 11, width - 80)
                for line in cont_lines:
                    c.drawString(50, y, line)
                    y -= 14
                    if y < 60:
                        c.showPage()
                        y = height - 80

                c.setFont("Helvetica-Bold", 12)
                c.drawString(40, y, f"Livello rischio: {livello.capitalize()}")
                y -= 30

            except Attacco.DoesNotExist:
                y -= 20

            if domande:
                c.setFont("Helvetica-Bold", 12)
                c.drawString(40, y, "Domande:")
                y -= 15
                c.setFont("Helvetica", 11)
                for domanda in domande:
                    c.drawString(60, y, f"- {domanda}")
                    y -= 14
                    if y < 60:
                        c.showPage()
                        y = height - 80

            y -= 30
            if y < 60:
                c.showPage()
                y = height - 80

    c.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="report_rilevamento_attacco.pdf")
