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
										  "placeholder": 'Entrez votre adresse mail'
										 },					   
								  )
		)
	password = base_form.CharField(
		label=_("Mot de passe"),

		strip=False,
		widget=base_form.PasswordInput(
									   attrs={
										"autocomplete": "current-password",
										"placeholder": 'Entrez votre mot de passe',
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
	Username = base_form.CharField(max_length=30,
							   label="Nom d'utilisateur",
						   	   required=True,
						   	   widget=base_form.TextInput(
							   attrs={'class': 'form-control'})
						  )
	name = base_form.CharField(max_length=100,
							   label='Nom',
						   	   required=True,
						   	   widget=base_form.TextInput(
							   attrs={'class': 'form-control'})
						  )
	email = base_form.EmailField(required=True,
								 label='Adresse Mail',
							 	 widget=base_form.TextInput(
								 attrs={'class': 'form-control'})
							)
	password = None
	class Meta(auth_forms.UserChangeForm.Meta):
		model = CustomUser
		fields = ("email", "name")
		field_classes = {"email": auth_forms.UsernameField}


class CustomUserCreationForm(auth_forms.UserCreationForm):
	"""
	A form that creates a user, with no privileges, from the given email and
	password.
	"""

	error_messages = {
		"password_mismatch": _("The two password fields didn’t match."),
	}
	name = base_form.CharField(max_length=100,
							   label='Nom',
							   required=True,
							   widget=base_form.TextInput(
							   attrs={'class': 'form-control',
							   		  'placeholder': 'Nom'})
						  	  )
	email = base_form.EmailField(required=True,
								 label='Email',
								 widget=base_form.TextInput(
								 attrs={'class': 'form-control',
								 		'placeholder': 'Adresse mail'})
								)
	password1 = base_form.CharField(
		label=_("Mot de Passe"),
		strip=False,
		widget=base_form.PasswordInput(attrs={
										"autocomplete": "new-password",
										"class": "form-control",
										"placeholder": "Mot de Passe",
										}),
		help_text="",
	)
	password2 = base_form.CharField(
		label=_("Confirmation du Mot de Passe"),
		widget=base_form.PasswordInput(attrs={
										"autocomplete": "new-password",
										"class": "form-control",
										"placeholder": "Confirmez le Mot de Passe",
										}),
		strip=False,
		help_text="",
	)

	class Meta(auth_forms.UserChangeForm.Meta):
		model = CustomUser
		fields = ("email", "name")
		field_classes = {"email": auth_forms.UsernameField}

class CustomPasswordResetForm(auth_forms.PasswordResetForm):
	email = base_form.EmailField(
		label="Email",
		max_length=254,
		widget=base_form.EmailInput(attrs={
									   "autocomplete": "email",
									   "class": "form-control",
									   'placeholder': 'Entrez votre adresse mail'}),
	)