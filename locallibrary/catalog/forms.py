
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, help_text='')
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(widget=forms.EmailInput)
     
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
