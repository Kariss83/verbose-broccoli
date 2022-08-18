""" This module is designed to host all the unit tests for the part of the
program in charge of parsing the sentence the user will pass to GrandPy.
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
from products.models import Categories, Favorites, Products

def mocked_send_mail():
	raise BadHeaderError


def create_an_user(number):
	user_test = CustomUser.objects.create(
			email=f"test{number}@gmail.com",
			name=f"MRTest{number}"
		)
	return user_test


class TestAccountsViewsModule(TestCase):
	""" Main class testing all the actions the parser is supposed to be able to
	achieve.
	"""
	@classmethod
	def setUpTestData(cls):
		cls.user = CustomUser.objects.create(
			email="test@gmail.com",
			name="MRTest",
		)
		cls.user.set_password('monsupermotdepasse')
		cls.user.save()

		cls.client = Client()

		cls.home_url = reverse('home:home')
		cls.register_url = reverse('users:register')
		cls.login_url = reverse('users:login')
		cls.logout_url = reverse('users:logout')
		cls.profile_url = reverse('users:profile')
		cls.edit_url = reverse('users:edit')

	def test_login_user_GET(self):
		response = self.client.get(self.login_url)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'registration/login.html')

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
		self.assertTemplateUsed(response, 'registration/register.html')

	def test_register_user_POST(self):
		response = self.client.post(
			self.register_url,
			{'email': 'test2@gmail.com',
			 'name': 'MRTest2',
			 'password1': 'monsupermotdepasse',
			 'password2': 'monsupermotdepasse'
			 },
			follow=True
			)
		new_user = CustomUser.objects.get(name='MRTest2')
		self.assertEqual(
			int(self.client.session['_auth_user_id']),
			new_user.id
			)
		self.assertEquals(response.status_code, 200)  
		self.assertTemplateUsed(response, 'home/index.html')

	def test_register_user_POST_invalid_form(self):
		response = self.client.post(
			'/users/register/',
			{'email': 'test2@gmail.com',
			 'password1': 'monsupermotdepasse',
			 },
			follow=True
			)
		messages = list(response.context['messages'])
		self.assertEqual(len(messages), 1)
		self.assertEqual(
			str(messages[0]),
			'Erreur de Création de Comptes - Veuillez reéssayer...')
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'registration/register.html')

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
		self.assertEqual(str(messages[0]), 'Vous êtes déconnecté(e)...')
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'home/index.html')

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
			 'name': 'MRTest3'
			 },
			follow=False
			)

		user.refresh_from_db()
		self.assertEqual(user.name, 'MRTest3')
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
			 'name': 'MRTest3'
			 },
			follow=True
			)

		user.refresh_from_db()
		self.assertEqual(user.name, 'MRTest3')
		self.assertEqual(user.email, 'test3@gmail.com')
		self.assertEqual(response.status_code, 200)  
		messages = list(response.context['messages'])
		self.assertEqual(len(messages), 1)
		self.assertEqual(str(messages[0]), 'Modifications enregistrées avec succès.')

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
			 'name': 'MRTest3'
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
			 'name': 'MRTest3'
			 },
			follow=True
			)
		self.assertEqual(response.status_code, 200)
		messages = list(response.context['messages'])
		self.assertEqual(len(messages), 1)
		self.assertEqual(str(messages[0]), 'Erreur de modification des informations, le formulaire n\'est pas valide')


class TestProductsViewsModule(TestCase):
	""" Main class testing all the actions the parser is supposed to be able to
	achieve.
	"""
	@classmethod
	def setUpTestData(cls):
		cls.user = create_an_user(1)
		cls.user.set_password('monsupermotdepasse')
		cls.user.save()
		cls.cat = create_a_category("Test")
		for i in range(10):
			create_a_product(i,
							 random.choice(["a", "b", "c", "d", "e"]),
							 cls.cat)
		cls.prod1, cls.prod2 = Products.objects.all()[:2]
		cls.fav1 = create_a_favorite(cls.user, cls.prod1, cls.prod2)

		cls.client = Client()

		cls.search_url = reverse('products:search')
		cls.savefavorite_url = reverse('products:savefavorite')
		cls.displayfavorite_url = reverse('products:displayfavorite')
		cls.product_url = reverse('products:productinfo')

	def test_search_product_GET(self):
		response = self.client.get(self.search_url)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'home/index.html')

	def test_search_product_POST(self):
		searched_prod = Products.objects.all()[0]
		response = self.client.post(
			self.search_url,
			{'searched': 'test0'},
			follow=True
			)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'search/search.html')
		self.assertTrue('searched_prod' in response.context)
		self.assertTrue('substitut_prods' in response.context)
		self.assertEqual(response.context['searched_prod'], searched_prod)
		self.assertEqual(len(response.context['substitut_prods']), 6)

	def test_info_product_GET(self):
		response = self.client.get(self.product_url)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'search/search.html')

	def test_info_product_POST(self):
		searched_prod = Products.objects.all()[0]
		response = self.client.post(
			self.product_url,
			{'prod_id': searched_prod.id},
			follow=True
			)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'products/product_info.html')
		self.assertTrue('product' in response.context)
		self.assertEqual(response.context['product'], searched_prod)

	def test_save_favorite_GET(self):
		self.client.login(
			email='test1@gmail.com',
			password='monsupermotdepasse'
			)
		response = self.client.get(self.savefavorite_url)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'search/search.html')

	def test_save_favorite_POST(self):
		self.client.login(
			email='test1@gmail.com',
			password='monsupermotdepasse'
			)
		searched_prod = Products.objects.all()[0]
		saved_prod = Products.objects.all()[5]
		response = self.client.post(
			self.savefavorite_url,
			{'favprod': saved_prod.id,
			 'searched_prod_id': searched_prod.id,
			 },
			follow=True
			)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'products/my_products.html')

		self.assertEqual(len(Favorites.objects.all()), 2)

	def test_show_favorite_GET(self):
		self.client.login(
			email='test1@gmail.com',
			password='monsupermotdepasse'
			)

		response = self.client.get(self.displayfavorite_url)

		self.assertEqual(str(response.context['user']), 'test1@gmail.com')
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'products/my_products.html')
		self.assertTrue('favorites' in response.context)
		self.assertNotEqual(len(response.context['favorites']), 0)
		self.assertEqual(response.context['favorites'][0], self.fav1)


class TestHomeViewsModule(TestCase):
	""" Class testing Home views.
	"""
	@classmethod
	def setUpTestData(cls):
		cls.user = CustomUser.objects.create(
			email="test@gmail.com",
			name="MRTest",
		)
		cls.user.set_password('monsupermotdepasse')
		cls.user.save()

		cls.client = Client()

		cls.pwd_reset_url = reverse('home:password_reset')

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
		self.assertEqual(str(messages[0]), 'Cet email est invalide.')
	
	def test_password_reset_POST_BadHeader(self):	
		with mock.patch("home.views.send_mail") as mocked_send_mail:
			mocked_send_mail.side_effect = BadHeaderError

			response = self.client.post(
				self.pwd_reset_url,
				{'email': 'test@gmail.com'},
				follow=True)

			self.assertTrue(mocked_send_mail.called)
			self.assertTrue('Invalid header found.' in str(response.content))