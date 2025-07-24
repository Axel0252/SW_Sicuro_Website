from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from .models import Attacco, Utente, ConsultazioneAttacco, EnciclopediaAttacchi, RilevamentoAttacco
from enciclopedia.views import generate_pdf_report
from django.utils.timezone import now


"""
class EnciclopediaAttacchiViewTest(TestCase):
    def setUp(self):
        # Crea una categoria enciclopedia per la FK
        self.categoria = EnciclopediaAttacchi.objects.create(categoria="Test Categoria")

        # Crea un attacco di test
        self.attacco = Attacco.objects.create(
            nome_attacco="Test Attacco",
            descrizione="Descrizione test\\ncon newline e \\ backslash",
            livello_rischio="basso",  # è obbligatorio, quindi lo devi passare
            contromisure="Consigli test\\ncon newline e \\ backslash",
            enciclopediaattacchi=self.categoria
        )

        # Crea un utente di test
        self.utente = Utente.objects.create(
            nome="Mario",
            cognome="Rossi",
            email="test@example.com",
            password="password123",
            tipo_utente="privato"
        )

        self.client = Client()

    def test_view_attacco_valido(self):
        # Testa che la pagina si carichi correttamente
        url = reverse('enciclopedia_attacchi', args=[self.attacco.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Descrizione")
        self.assertContains(response, "Contromisure")


    def test_view_attacco_non_esistente(self):
        url = reverse('enciclopedia_attacchi', args=[9999])  # id che non esiste
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_consultazione_creata_con_utente_in_sessione(self):
        # Inserisci l'id utente nella sessione
        session = self.client.session
        session['utente_id'] = self.utente.id
        session.save()

        url = reverse('enciclopedia_attacchi', args=[self.attacco.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Verifica che la consultazione sia stata salvata
        consultazioni = ConsultazioneAttacco.objects.filter(attacco=self.attacco, utente=self.utente)
        self.assertTrue(consultazioni.exists())

    def test_nessun_utente_in_sessione(self):
        url = reverse('enciclopedia_attacchi', args=[self.attacco.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Nessuna consultazione dovrebbe essere salvata
        consultazioni = ConsultazioneAttacco.objects.filter(attacco=self.attacco)
        self.assertFalse(consultazioni.exists())


class PdfReportTest(TestCase):
    def test_generate_pdf_report_basic(self):
        lista_esiti = [
            {
                'titolo': 'Test Attacco',
                'categoria': 'Phishing',
                'esito': 'Esito positivo',
                'descrizione': 'Descrizione test',
                'livello_rischio': 'alto',
                'contromisure': 'Usa antivirus aggiornato',
                'numero_si': 3,
                'totale_domande': 5,
            }
        ]

        class DummyUtente:
            nome = "Mario Rossi"

        utente = DummyUtente()

        pdf_file = generate_pdf_report(lista_esiti, utente)

        # Controlla che venga restituito un ContentFile
        self.assertIsInstance(pdf_file, ContentFile)

        # Controlla che il contenuto del PDF non sia vuoto
        self.assertTrue(len(pdf_file.read()) > 0)
"""



class RilevamentoAttaccoTestCase(TestCase):
    def setUp(self):
        # Crea un utente di test
        self.utente = Utente.objects.create(nome="Test Utente", email="test@example.com", password="testpass")
        # Crea un attacco di test con domande
        self.attacco = RilevamentoAttacco.objects.create(
            titolo="Test Attacco",
            categoria="Categoria Test",
            domande="Domanda 1\nDomanda 2\nDomanda 3",
            numero_domande = 3
        )
        self.client = Client()

    def test_access_without_login(self):
        # Accesso GET senza login (senza sessione)
        response = self.client.get(reverse('rilevamento_attacco'))
        self.assertContains(response, "Per eseguire questa funzionalità è necessario eseguire il login.")


    def test_access_with_login_get(self):
        # Simula login impostando la sessione
        session = self.client.session
        session['user_session_id'] = self.utente.id
        session.save()

        response = self.client.get(reverse('rilevamento_attacco'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("domande", response.context)

    def test_post_with_incomplete_answers(self):
        session = self.client.session
        session['user_session_id'] = self.utente.id
        session.save()

        # Mancano risposte per alcune domande
        post_data = {
            "domanda_0": "sì",
            # domanda_1 mancante
            "domanda_2": "no"
        }

        response = self.client.post(reverse('rilevamento_attacco'), data=post_data)
        self.assertContains(response, "Per favore, rispondi a tutte le domande.")

    def test_post_with_complete_answers_and_pdf_generation(self):
        session = self.client.session
        session['user_session_id'] = self.utente.id
        session.save()

        # Risposte valide per tutte le domande
        post_data = {
            "domanda_0": "sì",
            "domanda_1": "sì",
            "domanda_2": "no"
        }

        response = self.client.post(reverse('rilevamento_attacco'), data=post_data)
        # Dovrebbe reindirizzare a risultati_attacco
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('risultati_attacco'))

    def test_risultati_attacco_without_session(self):
        response = self.client.get(reverse('risultati_attacco'))
        # Senza sessione utente deve reindirizzare al login
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))

    def test_risultati_attacco_with_session(self):
        session = self.client.session
        session['user_session_id'] = self.utente.id
        session['esiti'] = [{
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
        session.save()

        response = self.client.get(reverse('risultati_attacco'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nessun attacco rilevato")
