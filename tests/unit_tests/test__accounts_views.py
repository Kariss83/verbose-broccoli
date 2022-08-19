""" This module is designed to host all the unit tests for the part of the
program in charge of handling user accounts.
"""
import random
from unittest import mock

from django.core.mail import BadHeaderError
from django.core import mail
from django.contrib import auth
from django.test import TestCase, Client
from django.urls import reverse

from accounts.forms import CustomAuthenticationForm

from accounts.models import CustomUser


def mocked_send_mail():
	raise BadHeaderError


def create_an_user(number):
	user_test = CustomUser.objects.create(
			email=f"test{number}@gmail.com",
			username=f"MRTest{number}"
		)
	return user_test


class TestAccountsViewsModule(TestCase):
	""" Main class testing hosting the tests.
	"""
	@classmethod
	def setUpTestData(cls):
		cls.user = CustomUser.objects.create(
			email="test@gmail.com",
			username="MRTest",
		)
		cls.user.set_password('monsupermotdepasse')
		cls.user.save()

		cls.client = Client()

		# cls.home_url = reverse('home:home')
		cls.register_url = reverse('accounts:register')
		cls.login_url = reverse('accounts:login')
		cls.logout_url = reverse('accounts:logout')
		cls.profile_url = reverse('accounts:profile')
		cls.edit_url = reverse('accounts:edit')
		cls.pwd_reset_url = reverse('accounts:password_reset')

	def test_login_user_GET(self):
		response = self.client.get(self.login_url)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'accounts/login.html')

	def test_login_user_POST(self):
		response = self.client.post(
			self.login_url,
			{'email': 'test@gmail.com', 'password': 'monsupermotdepasse'},
			)

		self.assertEqual(
			int(self.client.session['_auth_user_id']),
			self.user.id
			)
		self.assertEquals(response.status_code, 302)
		self.assertTrue(response.url.startswith('/'))

	def test_home_page_uses_item_form(self):
		response = self.client.get(self.login_url, follow=True)
		# import pdb; pdb.set_trace()
		self.assertIsInstance(
			response.context['form'],
			CustomAuthenticationForm
			)

	def test_login_user_POST_invalid_form(self):
		form = CustomAuthenticationForm(
			data={
				'email': '',
				'password': 'monsupermotdepasse'
				}
			)
		self.assertFalse(form.is_valid())
		self.assertEqual(
			form.errors['email'],
			["Ce champ est obligatoire."]
		)

	def test_register_user_GET(self):
		response = self.client.get(self.register_url)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'accounts/register.html')

	def test_register_user_POST(self):
		response = self.client.post(
			self.register_url,
			{'email': 'test2@gmail.com',
			 'username': 'MRTest2',
			 'password1': 'monsupermotdepasse',
			 'password2': 'monsupermotdepasse'
			 },
			follow=True
			)
		# import pdb; pdb.set_trace()
		new_user = CustomUser.objects.get(email='test2@gmail.com')
		self.assertEqual(
			int(self.client.session['_auth_user_id']),
			new_user.id
			)
		self.assertEquals(response.status_code, 200)  
		self.assertTemplateUsed(response, 'accounts/profile.html')

	def test_register_user_POST_invalid_form(self):
		response = self.client.post(
			'/accounts/register/',
			{'email': 'test2@gmail.com',
			 'password1': 'monsupermotdepasse',
			 },
			follow=True
			)
		messages = list(response.context['messages'])
		self.assertEqual(len(messages), 1)
		self.assertEqual(
			str(messages[0]),
			"""Account creation error (<ul class="errorlist"><li>username<ul class="errorlist"><li>Ce champ est obligatoire.</li></ul></li><li>password2<ul class="errorlist"><li>Ce champ est obligatoire.</li></ul></li></ul>)- Try Again...""")
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'accounts/register.html')

	def test_logout_user_GET(self):
		self.client.login(
			username='test@gmail.com',
			password='monsupermotdepasse'
			)
		user = auth.get_user(self.client)
		self.assertTrue(user.is_authenticated)

		response = self.client.get(self.logout_url, follow=True)

		messages = list(response.context['messages'])
		self.assertEqual(len(messages), 1)
		self.assertEqual(str(messages[0]), 'You are disconnected...')
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'accounts/login.html')

	def test_profile_user_logged_in_GET(self):
		self.client.login(
			email='test@gmail.com',
			password='monsupermotdepasse'
			)
		# import pdb; pdb.set_trace()
		response = self.client.get(self.profile_url)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'accounts/profile.html')

	def test_profile_GET_while_not_logged_in(self):
		response = self.client.get(self.profile_url)

		self.assertEquals(response.status_code, 302)
		self.assertTrue(response.url.startswith('/users/login/'))

	def test_edit_GET_while_not_logged_in(self):
		response = self.client.get(self.edit_url)

		self.assertEquals(response.status_code, 302)
		self.assertTrue(response.url.startswith('/users/login'))

	def test_edit_user_GET(self):
		self.client.login(
			username='test@gmail.com',
			password='monsupermotdepasse'
			)
		user = auth.get_user(self.client)
		self.assertTrue(user.is_authenticated)

		response = self.client.get(self.edit_url, follow=True)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'accounts/edit_profile.html')

	def test_edit_user_POST_without_follow(self):
		self.client.login(
			username='test@gmail.com',
			password='monsupermotdepasse'
			)
		user = auth.get_user(self.client)
		self.assertTrue(user.is_authenticated)

		response = self.client.post(
			self.edit_url,
			{'email': 'test3@gmail.com',
			 'username': 'MRTest3'
			 },
			follow=False
			)

		user.refresh_from_db()
		self.assertEqual(user.username, 'MRTest3')
		self.assertEqual(user.email, 'test3@gmail.com')
		self.assertEqual(response.status_code, 302)  

	def test_edit_user_POST_with_follow(self):
		self.client.login(
			username='test@gmail.com',
			password='monsupermotdepasse'
			)
		user = auth.get_user(self.client)
		self.assertTrue(user.is_authenticated)

		response = self.client.post(
			self.edit_url,
			{'email': 'test3@gmail.com',
			 'username': 'MRTest3'
			 },
			follow=True
			)

		user.refresh_from_db()
		self.assertEqual(user.username, 'MRTest3')
		self.assertEqual(user.email, 'test3@gmail.com')
		self.assertEqual(response.status_code, 200)  
		messages = list(response.context['messages'])
		self.assertEqual(len(messages), 1)
		self.assertEqual(str(messages[0]), 'Modification successfully saved')

	def test_edit_user_POST_invalid_form_no_follow(self):
		self.client.login(
			username='test@gmail.com',
			password='monsupermotdepasse'
			)
		user = auth.get_user(self.client)
		self.assertTrue(user.is_authenticated)

		response = self.client.post(
			self.edit_url,
			{'email': '',
			 'username': 'MRTest3'
			 },
			follow=False
			)
		self.assertEqual(response.status_code, 302)

	def test_edit_user_POST_invalid_form_(self):
		self.client.login(
			username='test@gmail.com',
			password='monsupermotdepasse'
			)
		user = auth.get_user(self.client)
		self.assertTrue(user.is_authenticated)

		response = self.client.post(
			self.edit_url,
			{'email': '',
			 'username': 'MRTest3'
			 },
			follow=True
			)
		self.assertEqual(response.status_code, 200)
		messages = list(response.context['messages'])
		self.assertEqual(len(messages), 1)
		self.assertEqual(str(messages[0]), 'There was an error in the form you filled, try again.')

	def test_password_reset_GET(self):
		response = self.client.get(self.pwd_reset_url)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'passwords/password_reset.html')

	def test_password_reset_POST(self):
		response = self.client.post(
			self.pwd_reset_url,
			{'email': 'test@gmail.com'},
			follow=True)
		self.assertEqual(len(mail.outbox), 1)
		self.assertEqual(mail.outbox[0].subject, 'Password Reset Requested')
		self.assertEqual(mail.outbox[0].from_email, 'root@vps-8351387e.vps.ovh.net')
		self.assertEqual(mail.outbox[0].to, ['test@gmail.com'])

	def test_password_reset_POST_invalid_address(self):
		response = self.client.post(
			self.pwd_reset_url,
			{'email': 'aezfazef@gmail.com'},
			follow=True)
		
		self.assertEqual(response.status_code, 200)
		messages = list(response.context['messages'])
		self.assertEqual(len(messages), 1)
		self.assertEqual(str(messages[0]), 'This email is invalid.')
	
	def test_password_reset_POST_BadHeader(self):	
		with mock.patch("accounts.views.send_mail") as mocked_send_mail:
			mocked_send_mail.side_effect = BadHeaderError

			response = self.client.post(
				self.pwd_reset_url,
				{'email': 'test@gmail.com'},
				follow=True)

			self.assertTrue(mocked_send_mail.called)
			self.assertTrue('Invalid header found.' in str(response.content))