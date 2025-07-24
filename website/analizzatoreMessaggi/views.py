from django.shortcuts import render

def analizzatoreIndex(request):
    if request.session.get('user_session_id'):
        return render(request, 'analizzatoreIndex.html')
    else:
        return render(request, 'analizzatoreIndex.html', {'error':"Per eseguire questa funzionalità è necessario eseguire il login."})

def checkMessage(request):
    SUSPICIOUS_KEYWORDS = [
        "password", "login", "verifica", "account", "urgente", "bloccato", "clicca qui", "collegamento",
        "aggiornare", "conferma", "sicurezza", "banca", "paypal", "hai vinto", "premio", "gratis",
        "bitcoin", "guadagna", "minaccia", "azione legale", "tempo limitato", "solo oggi"
    ]
    found_keywords=[]
    score = 0

    if request.method == 'POST':
        text = request.POST.get("text")

        for keyword in SUSPICIOUS_KEYWORDS:
            if keyword in text:
                found_keywords.append(keyword)
                score=score+1
        return render(request, 'analizzatoreIndex.html', {'score':score, 'found_keywords':found_keywords})
