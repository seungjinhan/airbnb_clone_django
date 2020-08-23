import uuid
from django.utils.translation import gettext_lazy
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.shortcuts import reverse


class User(AbstractUser):

    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"
    GENDER_CHOICES = (
        (GENDER_MALE, gettext_lazy("Male")),
        (GENDER_FEMALE, gettext_lazy("Female")),
        (GENDER_OTHER, gettext_lazy("Other")),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"
    LANGUAGE_CHOICES = ((LANGUAGE_ENGLISH, gettext_lazy("English")),
                        (LANGUAGE_KOREAN, gettext_lazy("Korean")))

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"
    CURRENCY_CHOICES = ((CURRENCY_USD, "Usd"), (CURRENCY_KRW, "Krw"))

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"
    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
    )

    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(gettext_lazy("gender"), choices=GENDER_CHOICES,
                              max_length=10, blank=True)
    bio = models.TextField(gettext_lazy("bio"), blank=True)
    birthdate = models.DateField(gettext_lazy(
        "birthdate"), blank=True, null=True)
    language = models.CharField(gettext_lazy("language"),
                                choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN)
    currency = models.CharField(gettext_lazy("currency"),
                                choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW)
    superhost = models.BooleanField(gettext_lazy("superhost"), default=False)
    email_verified = models.BooleanField(
        gettext_lazy("email_verified"), default=False)
    email_secret = models.CharField(gettext_lazy(
        "email_secret"), max_length=120, default='', blank=True)
    login_method = models.CharField(gettext_lazy("login_method"),
                                    choices=LOGIN_CHOICES, max_length=50, default=LOGIN_EMAIL)

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string(
                "email/verify.html", {'secret': secret})
            send_mail(
                gettext_lazy('verify airbnb'),
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message)
            self.save()
        return

    def __str__(self):
        return self.username
