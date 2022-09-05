from django import forms as base_form
from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext_lazy as _


from accounts.models import CustomUser


class CustomAuthenticationForm(base_form.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """

    email = base_form.EmailField(
        label='Email',
        widget=base_form.TextInput(
                                   attrs={
                                          "autofocus": True,
                                          "placeholder": 'Enter your email address'
                                         },
                                  )
        )
    password = base_form.CharField(
        label="Password",

        strip=False,
        widget=base_form.PasswordInput(
                                       attrs={
                                        "autocomplete": "current-password",
                                        "placeholder": 'Enter your password',
                                       }
                                      )
        )

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }


class CustomUserChangeForm(auth_forms.UserChangeForm):
    """
    A form to allow modification of the profile email adress and name.
    """
    username = base_form.CharField(max_length=30,
                                   label="Username",
                                   required=True,
                                   widget=base_form.TextInput(
                                   attrs={'class': 'form-control'}))

    email = base_form.EmailField(required=True,
                                 label='Email address',
                                 widget=base_form.TextInput(
                                 attrs={'class': 'form-control'}))
    password = None

    class Meta(auth_forms.UserChangeForm.Meta):
        model = CustomUser
        fields = ("email", "username")
        field_classes = {"email": auth_forms.UsernameField}


class CustomUserCreationForm(auth_forms.UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    username = base_form.CharField(max_length=100,
                                   label='Username :',
                                   required=True,
                                   widget=base_form.TextInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Enter your username'}))
    email = base_form.EmailField(required=True,
                                 label='Email :',
                                 widget=base_form.TextInput(
                                 attrs={'class': 'form-control',
                                        'placeholder': 'Enter a valid email address'}))
    password1 = base_form.CharField(
        label="Password :",
        strip=False,
        widget=base_form.PasswordInput(attrs={
                                        "autocomplete": "new-password",
                                        "class": "form-control",
                                        "placeholder": "Enter your password",
                                        }),
        help_text="",
    )
    password2 = base_form.CharField(
        label="Password confirmation :",
        widget=base_form.PasswordInput(attrs={
                                        "autocomplete": "new-password",
                                        "class": "form-control",
                                        "placeholder": "Confirm your password",
                                        }),
        strip=False,
        help_text="",
    )

    field_order = ['email', 'username', 'password1', 'password2', ]

    class Meta(auth_forms.UserChangeForm.Meta):
        model = CustomUser
        fields = ("email", "username")
        field_classes = {"email": auth_forms.UsernameField}


class CustomPasswordResetForm(auth_forms.PasswordResetForm):
    email = base_form.EmailField(
        label="Email",
        max_length=254,
        widget=base_form.EmailInput(attrs={
                                       "autocomplete": "email",
                                       "class": "form-control",
                                       'placeholder': 'Enter your email address'}),
    )
