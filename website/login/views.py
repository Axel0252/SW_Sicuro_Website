from django.shortcuts import render
from enciclopedia.models import *
import hashlib
from django.core.exceptions import ObjectDoesNotExist, ValidationError

def index(request):
    return render(request, 'loginIndex.html')

def checkLogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get('password')
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        try:
            user_data = Utente.objects.filter(email=email, password=hashed_password).get()
        except ObjectDoesNotExist:
            return render(request, 'loginIndex.html', {'error_message' : "Email e/o password non validi"})
        
        return render(request, 'homepage.html', {'data':user_data})
    
def registration(request):
    return render(request, 'sceltaUtente.html')

def registrazione_privato(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        utente = Utente.objects.filter(email=email)
        if len(utente) != 0:
            return render(request, 'registration.html', {'error_message':"Questa mail è già associata ad un altro utente."})
        password = request.POST.get('passw')
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        nome = request.POST.get('nome')
        cognome = request.POST.get('cognome')
        dataNascita = request.POST.get('dataNascita')

        utente = Utente.objects.create(
            email=email,
            password=hashed_password,
            dataNascita=dataNascita,
            nome=nome,
            cognome=cognome,
            tipo_utente="privato"
        )
        try:
            utente.full_clean() # Forza un controllo sull'aver inserito solo i valori consentiti
        except ValidationError:
            return render(request, 'index.html', {'error_message':"Dati inseriti non validi"})
        # If all good
        return render(request, 'index.html', {'success_message':"Registrazione avvenuta con successo"})
    else:
        return render(request, 'registration.html', {'error_message':"Problemi nella registrazione"}) # request error

def registrazione_azienda(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        utente = Utente.objects.filter(email=email)
        if len(utente) != 0:
            return render(request, 'registration.html', {'error_message':"Questa mail è già associata ad un altro utente."})
        password = request.POST.get('passw')
        hashed_password = hashlib.md5(password.encode()).hexdigest()
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
            utente.full_clean() # Forza un controllo sull'aver inserito solo i valori consentiti
        except ValidationError:
            return render(request, 'index.html', {'error_message':"Dati inseriti non validi"})
    
        return render(request, 'index.html', {'success_message':"Registrazione avvenuta con successo"})
    else:
        return render(request, 'registration.html', {'error_message':"Problemi nella registrazione"})

