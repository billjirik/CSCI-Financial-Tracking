
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from .models import IncomeSource, Expense

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, help_text='')
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(widget=forms.EmailInput)
     
    class Meta:
        model = User
        fields = ['username', 'email', 'password']



from django import forms
from .models import IncomeSource, Expense
from datetime import date

class IncomeAddForm(forms.ModelForm):
    class Meta:
        model = IncomeSource
        fields = ['name', 'amount', 'category', 'frequency', 'date']

    def clean_date(self):
        cleaned_data = super().clean()
        date_value = cleaned_data.get('date')
        if not date_value:
            return date.today()
        return date_value

class ExpenseAddForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'amount', 'category', 'frequency', 'date']

    def clean_date(self):
        cleaned_data = super().clean()
        date_value = cleaned_data.get('date')
        if not date_value:
            return date.today()
        return date_value
    
class ExpenseEditForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'amount', 'category', 'frequency', 'date']

class IncomeEditForm(forms.ModelForm):
    class Meta:
        model = IncomeSource
        fields = ['name', 'amount', 'category', 'frequency', 'date']

