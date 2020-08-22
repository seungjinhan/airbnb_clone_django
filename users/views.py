from django.contrib.auth.decorators import login_required
import os
import requests
from django.core.files.base import ContentFile
from django.views import View
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from . import forms, models, mixins


class LoginView(mixins.LoggedOutOnlyView, FormView):

    template_name = 'users/login.html'
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get('next')
        if next_arg is not None:
            return next_arg
        else:
            return reverse('core:home')
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
    messages.info(req, f'잘가요~!!')
    return redirect(reverse('core:home'))


class SignUpView(FormView):
    template_name = 'users/signup.html'
    form_class = forms.SignUpform
    success_url = reverse_lazy('core:home')

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


def github_login(req):
    client_id = os.environ.get('GITHUB_ID')
    redirect_uri = 'http://127.0.0.1:8000/users/login/github/callback'
    return redirect(f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user")


class GithubException(Exception):
    pass


def github_callback(req):
    try:
        client_id = os.environ.get('GITHUB_ID')
        client_secret = os.environ.get('GITHUB_SECRET')
        code = req.GET.get('code', None)
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"}
            )
            token_json = token_request.json()
            error = token_json.get('error', None)
            if error is not None:
                raise GithubException("Access Token 을 가져올수 없음")
            else:
                access_token = token_json.get('access_token')
                api_request = requests.get(
                    f"https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json", },)

                profile_json = api_request.json()
                username = profile_json.get('login', None)
                if username is not None:
                    name = profile_json.get('name')
                    email = profile_json.get('email')
                    bio = profile_json.get('bio')

                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException(
                                f"깃헙 로그인 계정이 아님: {user.login_method}")
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            email_verified=True,
                            login_method=models.User.LOGIN_GITHUB,)
                        user.set_unusable_password()
                        user.save()

                    login(req, user)
                    messages.success(req, f'환영합니다!!! {user.first_name}')

                    return redirect(reverse('core:home'))
                else:
                    raise GithubException("사용자 정보를 읽어 올수 없음")
        else:
            raise GithubException()
    except GithubException as e:
        messages.error(req, e)
        return redirect(reverse('users:login'))


def kakao_login(req):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code")


class KakaoException(Exception):
    pass


def kakao_callback(req):
    try:
        code = req.GET.get('code')
        raise KakaoException()
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}")
        token_json = token_request.json()
        err = token_json.get('error', None)

        if err is not None:
            raise KakaoException("Kakao token을 가져올수 없음")

        access_token = token_json.get('access_token')

        profile_request = requests.get(
            'https://kapi.kakao.com/v2/user/me', headers={"Authorization": f"Bearer {access_token}"})

        profile_json = profile_request.json()
        email = profile_json.get('kaccount_email', None)
        if email is None:
            raise KakaoException("Kakao Email이 없음")
        properties = profile_json.get("properties")
        nickname = properties.get('nickname')
        profile_image = properties.get('profile_image')
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"Kakao 로그인 계정이 아님 : {user.login_method}")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(f"{nickname}-avatar",
                                 ContentFile(photo_request.content))

        login(req, user)
        messages.success(req, f'환영합니다!!! {user.first_name}')
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(req, e)
        return redirect(reverse("users:login"))
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


class UserProfileView(DetailView):
    model = models.User
    context_object_name = "user_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UpdateUserProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        "first_name",
        "last_name",
        # "avatar",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )
    success_message = 'Profile 수정완료'

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['first_name'].widget.attrs = {'placeholder': 'First Name'}
        form.fields['last_name'].widget.attrs = {'placeholder': 'Last Name'}
        form.fields['bio'].widget.attrs = {'placeholder': 'Bio'}
        form.fields['birthdate'].widget.attrs = {'placeholder': 'Birthdate'}
        return form
    # def form_valid(self, form):
    #     email = form.cleaned_data.get('email')
    #     self.object.username = email
    #     self.object.save()
    #     return super().form_valid(form)


class UpdatePasswordView(
        mixins.LoggedInOnlyView,
        mixins.EmailLoginOnlyView,
        SuccessMessageMixin,
        PasswordChangeView):
    template_name = 'users/update-password.html'
    success_message = '패스워드 변경완료'

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['old_password'].widget.attrs = {
            'placeholder': 'Old Password'}
        form.fields['new_password1'].widget.attrs = {
            'placeholder': 'Password1'}
        form.fields['new_password2'].widget.attrs = {
            'placeholder': 'Password2'}

        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


@login_required
def switch_hosting(req):
    try:
        del req.session['is_hosting']
    except KeyError:
        req.session['is_hosting'] = True
    return redirect(reverse("core:home"))
