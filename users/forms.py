from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"placeholder": "Email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error(
                    'password', forms.ValidationError('Password wrong'))
        except models.User.DoesNotExist:
            self.add_error('email', forms.ValidationError("User not exist"))


class SignUpform(forms.ModelForm):

    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email", "birthdate")
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email Name"}),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError(
                "That email is already taken", code="existing_user"
            )
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        pw = self.cleaned_data.get('password')
        pw1 = self.cleaned_data.get('password1')

        if pw != pw1:
            raise forms.ValidationError('Password is Not match')
        else:
            return pw1

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user.username = email
        user.set_password(password)
        user.save()

# class SignUpform(forms.Form):

#     first_name = forms.CharField(max_length=80)
#     last_name = forms.CharField(max_length=80)
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)
#     password1 = forms.CharField(
#         widget=forms.PasswordInput, label='Confim Password')

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         try:
#             models.User.objects.get(email=email)
#             raise forms.ValidationError("Already User email")
#         except models.User.DoesNotExist:
#             return email

#     def clean_password1(self):
#         pw = self.cleaned_data.get('password')
#         pw1 = self.cleaned_data.get('password1')

#         if pw != pw1:
#             raise forms.ValidationError('Password is Not match')
#         else:
#             return pw1

#     def save(self):
#         first_name = self.cleaned_data.get('first_name')
#         last_name = self.cleaned_data.get('last_name')
#         email = self.cleaned_data.get('email')
#         password = self.cleaned_data.get('password')

#         user = models.User.objects.create_user(email,  email, password)
#         user.first_name = first_name
#         user.last_name = last_name
#         user.save()

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     try:
    #         models.User.objects.get(username=email)
    #         return email
    #     except models.User.DoesNotExist:
    #         raise forms.ValidationError("User not exist")

    # def clean_password(self):
    #     email = self.cleaned_data.get('email')
    #     password = self.cleaned_data.get('password')
    #     try:
    #         user = models.User.objects.get(username=email)
    #         if user.check_password(password):
    #             return password
    #         else:
    #             raise forms.ValidationError('Password wrong')
    #     except models.User.DoesNotExist:
    #         raise forms.ValidationError("User not exist")
