from django.test import TestCase, Client
from django.urls import reverse
from enciclopedia.models import NumeroTelefonico, RichiestaAnalisi

# Create your tests here.


class AnalisiNumeriViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('analisi_numeri')

    def test_numero_valido(self):
        """Numero valido e operatore riconosciuto"""
        response = self.client.post(self.url, {
            'prefisso': '+39',
            'numero': '3201234567'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "✅ Nessuna anomalia rilevata")
        self.assertContains(response, "Vodafone")
        self.assertContains(response, "Mobile")
        self.assertTrue(NumeroTelefonico.objects.filter(numero='+393201234567').exists())
        self.assertEqual(RichiestaAnalisi.objects.count(), 1)

    def test_numero_non_valido(self):
        """Prefisso mancante e numero non numerico"""
        response = self.client.post(self.url, {
            'prefisso': '0039',
            'numero': 'abc'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inserisci un numero valido")
        self.assertEqual(NumeroTelefonico.objects.count(), 0)
        self.assertEqual(RichiestaAnalisi.objects.count(), 0)

    def test_numero_sospetto(self):
        """Numero sospetto (finisce con 999 o inizia con +390)"""
        response = self.client.post(self.url, {
            'prefisso': '+39',
            'numero': '340123999'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "⚠️ Numero sospetto")
        self.assertContains(response, "TIM")
        self.assertContains(response, "Mobile")
        richiesta = RichiestaAnalisi.objects.first()
        self.assertEqual(richiesta.esito, "Sospetto")

    def test_sql_injection_attempt(self):
        """Tentativo di SQL Injection via numero"""
        response = self.client.post(self.url, {
            'prefisso': '+39',
            'numero': "321 OR 1=1"
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inserisci un numero valido con solo cifre e un prefisso selezionato."
)
        self.assertEqual(NumeroTelefonico.objects.count(), 0)
        self.assertEqual(RichiestaAnalisi.objects.count(), 0)

    def test_sql_injection_attempt_prefisso(self):
        """Tentativo SQL Injection via prefisso"""
        response = self.client.post(self.url, {
            'prefisso': "' OR '1'='1",
            'numero': "3211234567"
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inserisci un numero valido con solo cifre e un prefisso selezionato."
)
        self.assertEqual(NumeroTelefonico.objects.count(), 0)

"""
        def test_sql_injection_attempt_prefisso(self):
            response = self.client.post(self.url, {
                'prefisso': "+39' OR '1'='1",
                'numero': "3211234567"
            })

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Inserisci un numero valido con solo cifre e un prefisso selezionato."
                                )
            self.assertEqual(NumeroTelefonico.objects.count(), 0)

"""
