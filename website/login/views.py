from django.shortcuts import render
from enciclopedia.models import *
import hashlib
from django.core.exceptions import ObjectDoesNotExist # Gestisce sia DoesNotExist che MultipleObjectsReturned

def index(request):
    return render(request, 'loginIndex.html')

def checkLogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get('password')
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        try:
            user_data = Utente.objects.filter(email=email, password=hashed_password).get()
            reports = Esecuzione.objects.filter(utente=user_data.id).get()
        except ObjectDoesNotExist:
            return render(request, 'loginIndex.html', {'error_message' : "Email e/o password non validi"})
        
        return render(request, 'homepage.html', {'data':user_data, 'reports':reports})

