from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from enciclopedia.models import Utente

# Create your tests here.

class LoginViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')  # assicurati che il nome sia corretto nel tuo `urls.py`

        # Crea utente valido
        self.user = Utente.objects.create(
            email='test@example.com',
            password=make_password('password123'),
            data_nascita='1990-01-01',
            nome='Mario',
            cognome='Rossi',
            tipo_utente='privato',
            ruolo='privato'
        )

    def test_login_success(self):
        """Login con credenziali corrette"""
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'password123'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')
        self.assertIn('user_session_id', self.client.session)

    def test_login_email_errata(self):
        """Login con email non registrata"""
        response = self.client.post(self.login_url, {
            'email': 'wrong@example.com',
            'password': 'password123'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'loginIndex.html')
        self.assertContains(response, "Email e/o password non validi")
        self.assertEqual(self.client.session.get('failed_login_attempts'), 1)

    def test_login_password_errata(self):
        """Login con password errata"""
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'loginIndex.html')
        self.assertContains(response, "Email e/o password non validi")
        self.assertEqual(self.client.session.get('failed_login_attempts'), 1)

    def test_login_bloccato_dopo_tre_tentativi(self):
        """Blocca login dopo 3 tentativi falliti"""
        for i in range(3):
            response = self.client.post(self.login_url, {
                'email': 'test@example.com',
                'password': 'wrongpassword'
            })
        # Quarto tentativo bloccato
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })

        self.assertContains(response, "Hai superato il numero massimo di tentativi")
        self.assertEqual(self.client.session.get('failed_login_attempts'), 3)

    def test_login_get_request(self):
        """Un GET alla login view reindirizza"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('loginIndex'))  # se "loginIndex" è il nome della view
