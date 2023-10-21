from django.contrib.auth.forms import AuthenticationForm
from django import forms


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )


class CustomRegisterForm(forms.Form):
    register = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "btn btn-primary", "type": "submit", "value": "Register"}
        )
    )
