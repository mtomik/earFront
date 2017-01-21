from django.contrib.auth.forms import AuthenticationForm
from django import forms


# If you don't do this you cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))

class TrainerParams(forms.Form):
    first_param = forms.CharField(label='param1', max_length=100)

    second_param = forms.CharField(label='param2', max_length=100)

class CreateSamplesForm(forms.Form):
    positive_samples = forms.IntegerField(label='pos_samples', max_value=100000, min_value=10)