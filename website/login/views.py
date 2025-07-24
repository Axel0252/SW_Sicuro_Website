from django.shortcuts import render, redirect
from enciclopedia.models import *
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from .forms import privateRegistrazionForm, aziendaRegistrazionForm
from datetime import datetime
from django.utils import timezone
from datetime import timedelta

import logging
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'loginIndex.html')


def checkLogin(request):
    # Imposto la durata della sessione a 5 minuti (300 secondi)
    request.session.set_expiry(300)

    if request.method == "POST":
        # Recupero il contatore dei tentativi falliti dalla sessione, se non esiste è 0
        failed_attempts = request.session.get('failed_login_attempts', 0)

        # Blocca il login se i tentativi falliti sono >= 3
        if failed_attempts >= 3:
            return render(request, 'loginIndex.html', {
                'error_message': "Hai superato il numero massimo di tentativi. Riprova più tardi."
            })

        email = request.POST.get("email")
        password = request.POST.get('password')

        try:
            user_data = Utente.objects.filter(email=email).get()
        except Utente.DoesNotExist:
            # Incremento i tentativi falliti in sessione
            request.session['failed_login_attempts'] = failed_attempts + 1
            logger.info(str(timezone.now()) + " login errato: Email Errata (" + email + ")")
            return render(request, 'loginIndex.html', {'error_message': "Email e/o password non validi"})

        hashed_password = user_data.password

        if check_password(password, hashed_password):
            # Login corretto: resetto i tentativi falliti
            request.session['failed_login_attempts'] = 0
            request.session['user_session_id'] = user_data.id

            reports = Esecuzione.objects.filter(utente=user_data) \
                .select_related('rilevamento_attacco') \
                .order_by('-data_esecuzione', '-ora_esecuzione')

            consultazioni = ConsultazioneAttacco.objects.filter(utente=user_data) \
                .select_related('attacco') \
                .order_by('-data_consultazione', '-ora_consultazione')

            richieste = RichiestaAnalisi.objects.select_related('messaggio_sospetto', 'numero_telefonico') \
                .order_by('-data_richiesta', '-ora_richiesta')

            return render(request, 'homepage.html', {
                'data': user_data,
                'reports': reports,
                'consultazioni': consultazioni,
                'richieste': richieste
            })
        else:
            # Password errata: incremento i tentativi falliti
            request.session['failed_login_attempts'] = failed_attempts + 1
            return render(request, 'loginIndex.html', {'error_message': "Email e/o password non validi"})

    return redirect('loginIndex')


def render_homepage(request):

    user_id = request.session.get('user_session_id')
    if user_id:
        try:
            user_data = Utente.objects.get(id=user_id)
        except Utente.DoesNotExist:
            request.session.flush()
            return redirect('')

        reports = Esecuzione.objects.filter(utente=user_data) \
            .select_related('rilevamento_attacco') \
            .order_by('-data_esecuzione', '-ora_esecuzione')

        consultazioni = ConsultazioneAttacco.objects.filter(utente=user_data) \
            .select_related('attacco') \
            .order_by('-data_consultazione', '-ora_consultazione')

        richieste = RichiestaAnalisi.objects.select_related('messaggio_sospetto', 'numero_telefonico') \
            .order_by('-data_richiesta', '-ora_richiesta')

        return render(request, 'homepage.html', {
            'data': user_data,
            'reports': reports,
            'consultazioni': consultazioni,
            'richieste': richieste
        })
    else:
        return render(request, 'loginIndex.html', {'error_message' : "Esegui il login prima di accedere alla homepage"})


def registration(request):
    return render(request, 'sceltaUtente.html')


def registrazione_privato(request):
    if request.method == 'POST':
        form = privateRegistrazionForm(request.POST)
        email = request.POST.get('email')
        utente = Utente.objects.filter(email=email)
        if len(utente) != 0:
            return render(request, 'registra_privato.html', {'error_message':"Questa mail è già associata ad un altro utente."})

        if form.is_valid():
            hashed_password = make_password(form.cleaned_data['password'])

            utente = Utente.objects.create(
                email=form.cleaned_data['email'],
                password=hashed_password,
                data_nascita=form.cleaned_data['data_nascita'],
                nome=form.cleaned_data['nome'],
                cognome=form.cleaned_data['cognome'],
                tipo_utente='privato',
                ruolo='privato',
            )   
            try:
                utente.full_clean()
            except ValidationError:
                utente.delete()
                return render(request, 'loginIndex.html', {'error_message' : "Dati inseriti non validi"})
            
            return render(request, 'loginIndex.html', {'success_message':"Registrazione avvenuta con successo"})

    else:
        form = privateRegistrazionForm()
    return render(request, 'registra_privato.html', {'form':form})


def registrazione_azienda(request):
    if request.method == 'POST':
        form = aziendaRegistrazionForm(request.POST)
        email = request.POST.get('email')
        utente = Utente.objects.filter(email=email)
        if len(utente) != 0:
            return render(request, 'registra_privato.html', {'error_message':"Questa mail è già associata ad un altro utente."})

        if form.is_valid():
            hashed_password = make_password(form.cleaned_data['password'])

            utente = Utente.objects.create(
                email=form.cleaned_data['email'],
                password=hashed_password,
                data_nascita=form.cleaned_data['data_nascita'],
                nome=form.cleaned_data['nome'],
                cognome=form.cleaned_data['cognome'],
                tipo_utente='azienda',
                ruolo=form.cleaned_data['ruolo'],
                nome_azienda=form.cleaned_data['nome_azienda']
            )
            try:
                utente.full_clean()
            except ValidationError:
                utente.delete()
                return render(request, 'loginIndex.html', {'error_message' : "Dati inseriti non validi"})
            
            return render(request, 'loginIndex.html', {'success_message':"Registrazione avvenuta con successo"})

    else:
        form = aziendaRegistrazionForm()
    return render(request, 'registrazione_azienda.html', {'form':form})


def logoutUser(request):
    try:
        del request.session["user_session_id"]
    except KeyError:
        print("KeyError Exception")
        pass
    return redirect("loginIndex")
