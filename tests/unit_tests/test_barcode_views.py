"""This module is designed to host all the unit tests for the views of
the part of the program in charge of scanning and reading barcodes.
"""
import random
from unittest import mock

from django.contrib import auth
from django.test import TestCase, Client
from django.urls import reverse

class TestBarcodeViewsModule(TestCase):
	"""Main class hosting the tests.

	Args:
		TestCase (_type_): Default Test class
	"""
	@classmethod
	def setUpTestData(cls):
		cls.client = Client()

		cls.upload_url = reverse('barcode:upload')

	def test_upload_barcode_GET(self):
		response = self.client.get(self.upload_url)
		
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'barcode/upload.html')

	def test_upload_barcode_POST(self):
		pass