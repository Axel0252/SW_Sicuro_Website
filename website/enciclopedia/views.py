import os

from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.utils import timezone
from django.utils.timezone import now
from django.utils.html import escape, mark_safe
from django.conf import settings
from reportlab.platypus import Image, Paragraph, Spacer, SimpleDocTemplate

from enciclopedia.models import (
    EnciclopediaAttacchi,
    ConsultazioneAttacco,
    Attacco,
    RilevamentoAttacco,
    Utente,
    Esecuzione
)

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from django.core.files.base import ContentFile

from io import BytesIO



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

    utente_id = request.session.get('utente_id')
    if utente_id:
        try:
            utente = Utente.objects.get(id=utente_id)
            ConsultazioneAttacco.objects.create(
                attacco=attacco,
                utente=utente,
                ora_consultazione=timezone.now().time()
            )
            print("Consultazione salvata per utente:", utente.email)
        except Utente.DoesNotExist:
            print("Utente non trovato in sessione")
        except Exception as e:
            print("Errore salvataggio consultazione:", e)
    else:
        print("Nessun utente loggato in sessione")

    return render(request, 'enciclopedia_attacchi.html', {'attacco': attacco})





def rilevamento_attacco(request):
    def clean_testo(testo):
        return testo.replace('\\n', '\n').replace('\\', '').strip()

    utente_id = request.session.get('utente_id')
    if not utente_id:
        return redirect('login')

    try:
        utente = Utente.objects.get(id=utente_id)
    except Utente.DoesNotExist:
        return redirect('login')

    attacchi = RilevamentoAttacco.objects.all()
    tutte_domande = []
    index = 0

    # Prepara tutte le domande per il form
    for attacco in attacchi:
        domande_raw = attacco.domande.replace('\\n', '\n').replace('\\', '').strip()
        domande = domande_raw.split('\n')
        for domanda in domande:
            tutte_domande.append((index, attacco.id, domanda.strip()))
            index += 1

    if request.method == "POST":
        risposte = []
        for idx, attacco_id, domanda in tutte_domande:
            risposta = request.POST.get(f"domanda_{idx}")
            if risposta not in ["sì", "no", "non so"]:
                return render(request, "rilevamento_attacco.html", {
                    "domande": tutte_domande,
                    "error_msg": "Per favore, rispondi a tutte le domande."
                })
            risposte.append((attacco_id, risposta))

        risultati = {}
        for attacco_id, risposta in risposte:
            risultati.setdefault(attacco_id, []).append(risposta)

        esiti = []
        lista_dati_pdf = []
        data_corrente = now()

        for attacco in attacchi:
            risposte_attacco = risultati.get(attacco.id, [])
            num_si = risposte_attacco.count("sì")

            if num_si >= 2:
                try:
                    attacco_info = Attacco.objects.filter(nome_attacco__iexact=attacco.titolo).first()
                    print(f"Ricerca attacco: {attacco.titolo}")
                except Attacco.DoesNotExist:
                    attacco_info = None

                dati_pdf = {
                    "titolo": attacco.titolo,
                    "categoria": attacco.categoria,
                    "esito": f"Possibile attacco di tipo '{attacco.titolo}' rilevato.",
                    "numero_si": num_si,
                    "totale_domande": len(risposte_attacco),
                    "descrizione": clean_testo(attacco_info.descrizione) if attacco_info and attacco_info.descrizione else "Descrizione non disponibile",
                    "contromisure": clean_testo(attacco_info.contromisure) if attacco_info and attacco_info.contromisure else "Nessuna contromisura specificata",
                    "livello_rischio": attacco_info.livello_rischio if attacco_info and attacco_info.livello_rischio else "N/A",
                     "data": data_corrente.strftime("%d/%m/%Y"),
                    "ora": data_corrente.strftime("%H:%M:%S"),
                }


                lista_dati_pdf.append(dati_pdf)

                esiti.append({
                    "titolo": attacco.titolo,
                    "categoria": attacco.categoria,
                    "esito": dati_pdf["esito"],
                    "numero_si": num_si,
                    "totale_domande": len(risposte_attacco),
                    "descrizione": dati_pdf["descrizione"],
                    "livello_rischio": dati_pdf["livello_rischio"],
                    "contromisure": dati_pdf["contromisure"]
                })

        if not lista_dati_pdf:
            esiti.append({
                "titolo": "Nessun attacco rilevato",
                "categoria": "",
                "esito": "Non sono stati rilevati attacchi in base alle risposte fornite.",
                "numero_si": 0,
                "totale_domande": 0,
                "descrizione": "",
                "livello_rischio": "",
                "contromisure": ""

            })
        else:
            # Genera PDF unico e salvalo
            pdf_file = generate_pdf_report(lista_dati_pdf, utente)
            pdf_content = pdf_file
            pdf_nome = f"report_{utente.id}_{data_corrente.strftime('%Y%m%d_%H%M%S')}.pdf"

            # Crea una Esecuzione per ogni attacco rilevato
            for dati in lista_dati_pdf:
                try:
                    attacco_obj = RilevamentoAttacco.objects.get(titolo=dati["titolo"])
                except RilevamentoAttacco.DoesNotExist:
                    continue

                esecuzione = Esecuzione.objects.create(
                   rilevamento_attacco=attacco_obj,
                    utente=utente,
                    data_esecuzione=data_corrente,
                    ora_esecuzione=data_corrente.time()
                )
                esecuzione.pdf_report.save(pdf_nome, pdf_content)
                esecuzione.save()

                for e in esiti:
                    if e["titolo"] == dati["titolo"]:
                        e["pdf_url"] = esecuzione.pdf_report.url

        request.session["esiti"] = esiti
        return redirect(reverse("risultati_attacco"))

    return render(request, "rilevamento_attacco.html", {
        "domande": tutte_domande
    })


def risultati_attacco(request):
    utente_id = request.session.get('utente_id')
    if not utente_id:
        return redirect('login')

    esiti = request.session.get("esiti", [])

    if not esiti:
        esiti = [{
            "titolo": "Nessun attacco rilevato",
            "categoria": "",
            "esito": "Non sono stati rilevati attacchi in base alle risposte fornite.",
            "numero_si": 0,
            "totale_domande": 0,
            "pdf_url": None,
            "descrizione": "",
            "livello_rischio": "",
            "contromisure": ""
        }]

    return render(request, "risultati_attacco.html", {
        "esiti": esiti,
    })

def generate_pdf_report(lista_esiti, utente):

    def pulisci_testo_per_pdf(testo):
        if not testo:
            return "N/A"
        testo = testo.replace('\\ -', '\n-')
        testo = testo.replace('\\', '')
        testo = testo.strip()
        return testo

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='MyTitle', fontSize=18, leading=22, spaceAfter=12, alignment=1))
    styles.add(ParagraphStyle(name='Heading', fontSize=14, leading=18, spaceAfter=10))
    styles.add(ParagraphStyle(name='Text', fontSize=12, leading=15))

    logo_path = os.path.join(settings.BASE_DIR, 'website', 'static', 'img', 'logo2.png')
    logo = Image(logo_path, width=100, height=50)
    elements = []

    elements.append(logo)
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Report Rilevamento Attacchi", styles['MyTitle']))
    elements.append(Paragraph(f"Utente: {utente.nome}", styles['Text']))
    elements.append(Spacer(1, 12))

    for dati in lista_esiti:
        elements.append(Paragraph(f"TITOLO: {dati['titolo']}", styles['Heading']))
        elements.append(Paragraph(f"CATEGORIA: {dati['categoria']}", styles['Text']))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph(f"ESITO:", styles['Heading']))
        elements.append(Paragraph(pulisci_testo_per_pdf(dati['esito']), styles['Text']))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph(f"DESCRIZIONE:", styles['Heading']))
        elements.append(Paragraph(pulisci_testo_per_pdf(dati.get('descrizione', 'N/A')), styles['Text']))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph(f"LIVELLO DI RISCHIO:", styles['Heading']))
        elements.append(Paragraph(pulisci_testo_per_pdf(dati.get('livello_rischio', 'N/A')), styles['Text']))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph(f"CONTROMISURE:", styles['Heading']))
        elements.append(Paragraph(pulisci_testo_per_pdf(dati.get('contromisure', 'N/A')), styles['Text']))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph(f"Risposte Sì: {dati['numero_si']} / {dati['totale_domande']}", styles['Text']))
        elements.append(Spacer(1, 24))

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return ContentFile(pdf)
