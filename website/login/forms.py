from django import forms
import re
from django.core.exceptions import ValidationError

class privateRegistrazionForm(forms.Form):
    nome = forms.CharField(max_length=15)
    cognome = forms.CharField(max_length=15)
    email = forms.EmailField(max_length=35, min_length=11)
    data_nascita = forms.DateField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise ValidationError("La password deve contenere almeno 8 caratteri.")
        if not re.search(r"[A-Z]", password):
            raise ValidationError("La password deve contenere almeno una lettera maiuscola.")
        if not re.search(r"[a-z]", password):
            raise ValidationError("La password deve contenere almeno una lettera minuscola.")
        if not re.search(r"[0-9]", password):
            raise ValidationError("La password deve contenere almeno un numero.")
        if not re.search(r"[!@#$%^&*]", password):
            raise ValidationError("La password deve contenere almeno un simbolo (!@#$%^&*).")

        return password

class aziendaRegistrazionForm(forms.Form):
    nome = forms.CharField(max_length=15)
    cognome = forms.CharField(max_length=15)
    email = forms.EmailField(max_length=35, min_length=11)
    data_nascita = forms.DateField()
    nome_azienda = forms.CharField(max_length=15)
    ruolo = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise ValidationError("La password deve contenere almeno 8 caratteri.")
        if not re.search(r"[A-Z]", password):
            raise ValidationError("La password deve contenere almeno una lettera maiuscola.")
        if not re.search(r"[a-z]", password):
            raise ValidationError("La password deve contenere almeno una lettera minuscola.")
        if not re.search(r"[0-9]", password):
            raise ValidationError("La password deve contenere almeno un numero.")
        if not re.search(r"[!@#$%^&*]", password):
            raise ValidationError("La password deve contenere almeno un simbolo (!@#$%^&*).")

        return password
