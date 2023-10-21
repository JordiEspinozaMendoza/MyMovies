from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms
from django.contrib.auth.models import User


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


class CustomSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class MovieReviewForm(forms.Form):
    rating = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Rating (1-100)"}
        ),
    )
    review = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Write your review here..."}
        ),
    )
