from django.shortcuts import render
from datetime import datetime
import requests
from enciclopedia.models import *

def numeri_index(request):
    if request.session.get('user_session_id'):
        return render(request, 'analisi_numeri.html')
    else:
        return render(request, 'analisi_numeri.html', {'message':"Per eseguire questa funzionalità è necessario eseguire il login."})

def analisi_numeri(request):
    result = None
    message = None
    
    if request.method == "POST":
        prefisso = request.POST.get("prefisso", "")
        numero_parziale = request.POST.get("numero", "").strip()

        numero = prefisso + numero_parziale

        if not prefisso.startswith("+") or not numero_parziale.isdigit():
            message = "Inserisci un numero valido con solo cifre e un prefisso selezionato."
        else:
            corpo_numero = numero.replace(prefisso, "")
            primo_blocco = corpo_numero[:3]

            operatori = {
                "320": "Vodafone",
                "327": "Vodafone",
                "323": "Vodafone",
                "340": "TIM",
                "349": "TIM",
                "351": "Iliad",
                "352": "Iliad",
                "353": "Iliad",
                "355": "Iliad",
                "356": "Iliad",
                "357": "Iliad",
                "366": "WindTre",
                "368": "WindTre",
                "377": "PosteMobile",
                "370": "Fastweb",
                "373": "CoopVoce",
                "081": "TIM Fisso",
                "02": "Telecom Milano",
                "06": "Telecom Roma"
            }

            operatore = operatori.get(primo_blocco, "Operatore sconosciuto")
            tipo = "mobile" if primo_blocco.startswith("3") else "fisso"
            sospetto = numero.endswith("999") or numero.startswith("+390")

            numero_obj, _ = NumeroTelefonico.objects.get_or_create(
                numero=numero,
                defaults={
                    "tipo": tipo,
                    "operatore": operatore
                }
            )

            RichiestaAnalisi.objects.create(
                numero_telefonico=numero_obj,
                ora_richiesta=datetime.now().time(),
                esito="Sospetto" if sospetto else "Pulito"
            )

            result = {
                "numero": numero,
                "valido": "Sì",
                "sospetto": "Sì" if sospetto else "No",
                "esito": "⚠️ Numero sospetto" if sospetto else "✅ Nessuna anomalia rilevata",
                "operatore": operatore,
                "tipo": tipo.capitalize()
            }

        return render(request, "analisi_numeri.html", {
            "result": result,
            "message": message
        })
