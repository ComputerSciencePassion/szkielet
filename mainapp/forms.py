from django import forms
from django.forms import DateInput, TimeInput, CheckboxSelectMultiple
from django.contrib.auth.forms import UserCreationForm
from .models import Atrakcja
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField
from django.contrib.auth.models import User

class UserRegForm(UserCreationForm):
    username = forms.CharField(label='Nazwa użytkownika', widget=forms.TextInput(attrs={'id': 'username'}))
    e_mail = forms.EmailField(required=True, label='Adres E-mail', error_messages={'invalid': 'Wprowadź poprawny adres email.'}, widget=forms.EmailInput(attrs={'id': 'email'}))
    password1 = forms.CharField(label='Wpisz hasło', widget=forms.PasswordInput(attrs={'id': 'password1'}))
    password2 = forms.CharField(label='Wpisz ponownie hasło', widget=forms.PasswordInput(attrs={'id': 'password2'}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={'id': 'captcha'}), label='')
    class Meta:
        model = User
        fields = ['username', 'e_mail', 'password1', 'password2', 'captcha']
        
class planowanie(forms.Form):
    miasto=forms.CharField()
    ulica=forms.CharField()
    data_od=forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    data_do=forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    KATEGORIE_CHOICES = forms.MultipleChoiceField(choices=Atrakcja.KATEGORIE_CHOICES, widget=forms.CheckboxSelectMultiple)