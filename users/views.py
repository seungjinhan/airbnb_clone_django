from django.views import View
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms


class LoginView(View):

    def get(self, req):
        form = forms.LoginForm(initial={'email': 'hanblues@gmail.com'})
        return render(req, 'users/login.html', {'form': form})

    def post(self, req):
        form = forms.LoginForm(req.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(req, username=email, password=password)
            if user is not None:
                login(req, user)
                return redirect(reverse('core:home'))

        return render(req, 'users/login.html', {'form': form})


def log_out(req):
    logout(req)
    return redirect(reverse('core:home'))
