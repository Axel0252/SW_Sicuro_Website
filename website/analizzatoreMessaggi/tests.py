from django.test import TestCase, Client
from django.urls import reverse

class CheckMessageTestCase(TestCase):
    def setUp(self):
        self.client = Client()


    def test_no_suspicious_keywords(self):
        response = self.client.post(reverse('checkMessage'), {'text': 'Questo è un messaggio innocuo.'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['score'], 0)
        self.assertEqual(response.context['found_keywords'], [])

    def test_found_suspicious_keywords(self):
        text = "Devi aggiornare la password e clicca qui subito."
        response = self.client.post(reverse('checkMessage'), {'text': text})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['score'], 3)
        self.assertIn('password', response.context['found_keywords'])
        self.assertIn('clicca qui', response.context['found_keywords'])

    def test_case_sensitive_keywords(self):
        text = "Hai VINTO un premio!"
        response = self.client.post(reverse('checkMessage'), {'text': text.lower()})  # la tua ricerca è case sensitive?
        self.assertEqual(response.status_code, 200)
        self.assertIn('premio', response.context['found_keywords'])

    def test_sql_injection_attempt(self):
        injection_string = "1 OR 1=1; DROP TABLE users;"  # stringa tipica di SQL injection
        response = self.client.post(reverse('checkMessage'), {'text': injection_string})
        self.assertEqual(response.status_code, 200)
        # Non dovrebbe trovare parole sospette (perché la tua ricerca è su parole chiave precise)
        self.assertEqual(response.context['score'], 0)
        self.assertEqual(response.context['found_keywords'], [])

    def test_empty_post(self):
        response = self.client.post(reverse('checkMessage'), {'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['score'], 0)
        self.assertEqual(response.context['found_keywords'], [])

