from django.db import models

class Utente(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)  # emailfield verifica tutti i requisiti di un indirizzo email
    password = models.CharField(max_length=128)
    tipo_utente = models.CharField(max_length=50, choices=[
        ('privato', 'Privato'),
        ('azienda', 'Aziendale')
    ], default='azienda')
    nome_azienda = models.CharField(max_length=100, blank=True, null=True)
    ruolo = models.CharField(max_length=50)
    data_nascita = models.DateField(blank=True, null=True)
    eta = models.IntegerField(blank=True, null=True)

class RilevamentoAttacco(models.Model):
    id = models.AutoField(primary_key=True)
    titolo = models.CharField(max_length=255)
    domande = models.TextField()
    numero_domande = models.IntegerField()
    categoria = models.CharField(max_length=100)
    pdf_report = models.FileField(upload_to="pdf_reports/", blank=True, null=True)

class Esecuzione(models.Model):
    id = models.AutoField(primary_key=True)
    rilevamento_attacco = models.ForeignKey(RilevamentoAttacco, on_delete=models.CASCADE)
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE)
    data_esecuzione = models.DateTimeField(auto_now_add=True)
    ora_esecuzione= models.TimeField()
    pdf_report = models.FileField(upload_to='pdf_reports/', blank=True, null=True)

class MessaggioSospetto(models.Model):
    id = models.AutoField(primary_key=True)
    testo = models.TextField()
    data_ricezione = models.DateTimeField(auto_now_add=True)
    mittente = models.CharField(max_length=255)

class NumeroTelefonico(models.Model):
    id = models.AutoField(primary_key=True)
    numero = models.CharField(max_length=20, unique=True)
    operatore = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=[
        ('mobile', 'Mobile'),
        ('fisso', 'Fisso')
    ], default='mobile')

class RichiestaAnalisi(models.Model):
    id = models.AutoField(primary_key=True)
    messaggio_sospetto = models.ForeignKey(MessaggioSospetto, on_delete=models.CASCADE, null=True, blank=True)
    numero_telefonico = models.ForeignKey(NumeroTelefonico, on_delete=models.CASCADE, null=True, blank=True)
    data_richiesta = models.DateTimeField(auto_now_add=True)
    ora_richiesta = models.TimeField()
    esito = models.TextField()

class EnciclopediaAttacchi(models.Model):
    id = models.AutoField(primary_key=True)
    categoria = models.CharField(max_length=100)  # Categoria dell'attacco, ad esempio "Phishing", "Malware", ecc.

class Attacco(models.Model):
    id = models.AutoField(primary_key=True)
    nome_attacco = models.CharField(max_length=255)
    descrizione = models.TextField()
    livello_rischio = models.CharField(
        max_length=100,
        choices=[
            ('basso', 'Basso'),
            ('medio', 'Medio'),
            ('alto', 'Alto')
        ],
        default='basso',
        null=False,
        blank=False
    )
    contromisure = models.TextField()
    enciclopediaattacchi = models.ForeignKey(EnciclopediaAttacchi, on_delete=models.CASCADE)

class ConsultazioneAttacco(models.Model):
    id = models.AutoField(primary_key=True)
    attacco = models.ForeignKey(Attacco, on_delete=models.CASCADE)
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE)
    data_consultazione = models.DateTimeField(auto_now_add=True)
    ora_consultazione = models.TimeField()