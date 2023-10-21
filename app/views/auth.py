from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from app.forms import CustomLoginForm, CustomSignUpForm
from django.contrib.auth import login


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = "login.html"


def CustomSignUpView(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = CustomSignUpForm()

    return render(request, "sign_up.html", {"form": form})
