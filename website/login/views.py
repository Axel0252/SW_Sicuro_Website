from django.shortcuts import render
from enciclopedia.models import *
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction
from .forms import privateRegistrazionForm

def index(request):
    return render(request, 'loginIndex.html')

def checkLogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get('password')

        try:
            user_data = Utente.objects.filter(email=email).get()
        except ObjectDoesNotExist:
            return render(request, 'loginIndex.html', {'error_message' : "Email e/o password non validi"})
        
        hashed_password = user_data.password

        if check_password(password, hashed_password):
            reports = list(Esecuzione.objects.select_related('utente', 'rilevamento_attacco'))
            return render(request, 'homepage.html', {'data':user_data, 'reports':reports})
        else:
            return render(request, 'loginIndex.html', {'error_message' : "Email e/o password non validi"})


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
            hashed_password = make_password(form.password)

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
        email = request.POST.get('email')
        utente = Utente.objects.filter(email=email)
        if len(utente) != 0:
            return render(request, 'registrazione_azienda.html', {'error_message':"Questa mail è già associata ad un altro utente."})
        password = request.POST.get('passw')
        hashed_password = make_password(password)
        nome = request.POST.get('nome')
        cognome = request.POST.get('cognome')
        dataNascita = request.POST.get('dataNascita')
        nome_azienda = request.POST.get('nomeAzienda')
        ruolo = request.POST.get('ruolo')

        utente = Utente.objects.create(
            email=email,
                password=hashed_password,
                dataNascita=dataNascita,
                nome=nome,
                cognome=cognome,
                tipo_utente="azienda",
                nome_azienda=nome_azienda,
                ruolo=ruolo
        )

        try:
            utente.full_clean()
        except ValidationError:
            transaction.rollback()
            return render(request, 'loginIndex.html', {'error_message' : "Dati inseriti non validi"})
        
        return render(request, 'loginIndex.html', {'success_message':"Registrazione avvenuta con successo"})
    
    else:
        return render(request, 'registrazione_azienda.html', {'error_message':"Problemi nella registrazione"})

def scelta_privato(request):
    return render(request, 'registra_privato.html')

def scelta_azienda(request):
    return render(request, 'registrazione_azienda.html')