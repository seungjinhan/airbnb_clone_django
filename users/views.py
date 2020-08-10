from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms, models


class LoginView(FormView):

    template_name = 'users/login.html'
    form_class = forms.LoginForm
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    # def post(self, req):
    #     form = forms.LoginForm(req.POST)

    #     if form.is_valid():
    #         email = form.cleaned_data.get('email')
    #         password = form.cleaned_data.get('password')
    #         user = authenticate(req, username=email, password=password)
    #         if user is not None:
    #             login(req, user)
    #             return redirect(reverse('core:home'))

    #     return render(req, 'users/login.html', {'form': form})


def log_out(req):
    logout(req)
    return redirect(reverse('core:home'))


class SignUpView(FormView):
    template_name = 'users/signup.html'
    form_class = forms.SignUpform
    success_url = reverse_lazy('core:home')
    initial = {
        'first_name': 'Han',
        'last_name': 'Jimmy',
        'email': 'hanblues@kakao.com',
    }

    def form_valid(self, form):

        form.save()

        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)

        user.verify_email()

        return super().form_valid(form)


def complete_verify(req, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ''
        user.save()
    except models.User.DoesNotExist:
        pass

    return redirect(reverse('core:home'))

# class LoginView(View):

#     def get(self, req):
#         form = forms.LoginForm(initial={'email': 'hanblues@gmail.com'})
#         return render(req, 'users/login.html', {'form': form})

#     def post(self, req):
#         form = forms.LoginForm(req.POST)

#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             user = authenticate(req, username=email, password=password)
#             if user is not None:
#                 login(req, user)
#                 return redirect(reverse('core:home'))

#         return render(req, 'users/login.html', {'form': form})


# def log_out(req):
#     logout(req)
#     return redirect(reverse('core:home'))
