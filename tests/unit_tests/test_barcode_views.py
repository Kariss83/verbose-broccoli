"""This module is designed to host all the unit tests for the views of
the part of the program in charge of scanning and reading barcodes.
"""
import os
from unittest import mock
from datetime import datetime, timedelta

from django.test import TestCase, Client
from django.urls import reverse

from . import constants
from gamezscan.collection.models import Game, Collection
from gamezscan.accounts.models import CustomUser
from gamezscan.datafetcher import constants as cst
from gamezscan.datafetcher.oauthclient.model.model import oAuth_token


def create_an_user(number):
    user_test = CustomUser.objects.create(
        email=f"test{number}@gmail.com", username=f"MRTest{number}"
    )
    return user_test


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if "https://product-lookup-by-upc-or-ean.p.rapidapi.com/code/" in args[0]:
        return MockResponse(cst.EAN_API_RETURN, 200)
    elif args[0] == "https://api.ebay.com/buy/browse/v1/item_summary/search?":
        return MockResponse(cst.EBAY_RETURN, 200)

    return MockResponse(None, 404)


def mocked_get_application_token(*args, **kwargs):
    token = oAuth_token()
    token.access_token = "myfaketoken"
    token.token_expiry = datetime.utcnow() + timedelta(hours=5) - timedelta(minutes=5)
    return token


def mocked_credential_load(*args, **kwargs):
    pass


class TestBarcodeViewsModule(TestCase):
    """Main class hosting the tests.

    Args:
        TestCase (_type_): Default Test class
    """

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        cls.user = CustomUser.objects.create(
            email="test@gmail.com",
            username="MRTest",
        )
        cls.user.set_password("monsupermotdepasse")
        cls.user.save()

        Collection.objects.create(name="My First Collection", user=cls.user)
        cls.collections = Collection.objects.filter(user=cls.user)

        cls.upload_url = reverse("barcode:upload")

    def test_upload_barcode_GET(self):
        response = self.client.get(self.upload_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "barcode/scan.html")

    @mock.patch(
        "gamezscan.datafetcher.oauthclient.oauth2api.oauth2api.get_application_token",
        side_effect=mocked_get_application_token,
    )
    @mock.patch(
        "gamezscan.datafetcher.oauthclient.credentialutil.credentialutil.load",
        side_effect=mocked_credential_load,
    )
    @mock.patch(
        "gamezscan.datafetcher.fetcher.requests.get", side_effect=mocked_requests_get
    )
    def test_upload_barcode_POST_file_not_logged_in(
        self, mocked_get_application_token, mocked_credential_load, mocked_requests_get
    ):
        cwd = os.getcwd()
        image_path = os.path.join(cwd, "tests/unit_tests/media_test/barcode.png")
        with open(image_path, "rb") as f:
            response = self.client.post(self.upload_url, {"file": f}, follow=True)
            self.assertTrue(
                "Le Seigneur des anneaux - La guerre du Nord" in str(response.content)
            )
            self.assertEquals(response.status_code, 200)

    def test_upload_barcode_POST_file_too_large_not_logged_in(self):
        cwd = os.getcwd()
        image_path = os.path.join(cwd, "tests/unit_tests/media_test/too_big.png")
        with open(image_path, "rb") as f:
            response = self.client.post(self.upload_url, {"file": f}, follow=True)
            messages = list(response.context["messages"])
            self.assertEqual(len(messages), 1)
            self.assertEqual(
                "File too large. Size should not exceed 10 MiB.", str(messages[0])
            )
            self.assertEquals(response.status_code, 200)
            self.assertEquals(response.status_code, 200)

    @mock.patch(
        "gamezscan.datafetcher.oauthclient.oauth2api.oauth2api.get_application_token",
        side_effect=mocked_get_application_token,
    )
    @mock.patch(
        "gamezscan.datafetcher.oauthclient.credentialutil.credentialutil.load",
        side_effect=mocked_credential_load,
    )
    @mock.patch(
        "gamezscan.datafetcher.fetcher.requests.get", side_effect=mocked_requests_get
    )
    def test_upload_barcode_POST_file_logged_in(
        self, mocked_get_application_token, mocked_credential_load, mocked_requests_get
    ):
        self.client.login(email="test@gmail.com", password="monsupermotdepasse")
        cwd = os.getcwd()
        image_path = os.path.join(cwd, "tests/unit_tests/media_test/barcode.png")
        with open(image_path, "rb") as f:
            response = self.client.post(self.upload_url, {"file": f}, follow=True)
            self.assertQuerysetEqual(
                self.collections, response.context[0].dicts[-1]["collections"]
            )
            self.assertEquals(response.status_code, 200)

    def test_upload_barcode_POST_file_not_logged_no_barcode(self):
        cwd = os.getcwd()
        image_path = os.path.join(cwd, "tests/unit_tests/media_test/no_barcode.png")
        with open(image_path, "rb") as f:
            response = self.client.post(self.upload_url, {"file": f}, follow=True)
            messages = list(response.context["messages"])
            self.assertEqual(len(messages), 1)
            self.assertEqual("No barcode detected - Try again...", str(messages[0]))
            self.assertEquals(response.status_code, 200)

    @mock.patch(
        "gamezscan.datafetcher.oauthclient.oauth2api.oauth2api.get_application_token",
        side_effect=mocked_get_application_token,
    )
    @mock.patch(
        "gamezscan.datafetcher.oauthclient.credentialutil.credentialutil.load",
        side_effect=mocked_credential_load,
    )
    @mock.patch(
        "gamezscan.datafetcher.fetcher.requests.get", side_effect=mocked_requests_get
    )
    def test_can_upload_using_webcam_not_logged_in(
        self, mocked_get_application_token, mocked_credential_load, mocked_requests_get
    ):
        response = self.client.post(
            self.upload_url, {"b64img": constants.B64STRING}, follow=True
        )
        game = Game.objects.get(name="Le Seigneur des anneaux - La guerre du Nord")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(game, response.context[0].dicts[-1]["game"])

    @mock.patch(
        "gamezscan.datafetcher.oauthclient.oauth2api.oauth2api.get_application_token",
        side_effect=mocked_get_application_token,
    )
    @mock.patch(
        "gamezscan.datafetcher.oauthclient.credentialutil.credentialutil.load",
        side_effect=mocked_credential_load,
    )
    @mock.patch(
        "gamezscan.datafetcher.fetcher.requests.get", side_effect=mocked_requests_get
    )
    def test_can_upload_using_webcam_logged_in(
        self, mocked_get_application_token, mocked_credential_load, mocked_requests_get
    ):
        self.client.login(email="test@gmail.com", password="monsupermotdepasse")
        response = self.client.post(
            self.upload_url, {"b64img": constants.B64STRING}, follow=True
        )
        self.assertQuerysetEqual(
            self.collections, response.context[0].dicts[-1]["collections"]
        )
        self.assertEquals(response.status_code, 200)

    def test_can_upload_using_webcam_not_logged_in_no_barcode(self):
        response = self.client.post(
            self.upload_url, {"b64img": constants.B64NOBARCODE}, follow=True
        )
        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual("No barcode detected - Try again...", str(messages[0]))
        self.assertEquals(response.status_code, 200)
