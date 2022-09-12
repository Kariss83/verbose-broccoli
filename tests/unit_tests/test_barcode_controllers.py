""" This module is designed to host all the unit tests for the part of the
program in charge of handling barcode reading either from a file or using
the camera/webcam.
"""
import os
from unittest import mock
from datetime import datetime, timedelta

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from barcode.controllers.barcode_reader import ImageReader, Stringb64Reader
from barcode.controllers.information_gatherer import Gatherer
from datafetcher.oauthclient.model.model import oAuth_token
from datafetcher import constants as cst
from . import constants


class TestBarcodeReaderModule(TestCase):
    """Main class testing hosting the tests."""

    @classmethod
    def setUpTestData(cls):
        cwd = os.getcwd()
        image_path = os.path.join(cwd, "tests/unit_tests/media_test/barcode.png")
        cls.file_return = SimpleUploadedFile(
            name="barcode.png",
            content=open(image_path, "rb").read(),
            content_type="image/png",
        )

    def test_ImageReader_can_read_barcode_from_file(self):
        reader = ImageReader(self.file_return)
        barcode = reader.get_image_barcode()
        self.assertTrue(str(barcode[0]) == "0710425471254")

    def test_b64Reader_can_save_string_to_png(self):
        reader = Stringb64Reader(constants.B64STRING)
        self.assertTrue(reader.img is None)
        reader.string_to_PNG()
        self.assertTrue(reader.img is not None)

    def test_b64Reader_can_handle_bad_padding(self):
        reader = Stringb64Reader(constants.B64STRING_MISSING_PADDING)
        missing_padding = len(reader.img_data_str.split(",")[1]) % 4
        self.assertTrue(missing_padding != 0)
        reader.string_to_PNG()
        missing_padding = len(reader.img_data_str) % 4
        self.assertTrue(missing_padding == 0)

    def test_b64Reader_can_retrieve_barcode(self):
        reader = Stringb64Reader(constants.B64STRING)
        reader.string_to_PNG()
        barcodes = reader.read_image()
        self.assertEqual(str(barcodes[0]), "0710425471254")


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


class TestInformationGathererModule(TestCase):
    """Main class testing hosting the tests."""

    @classmethod
    def setUpTestData(cls):
        cwd = os.getcwd()
        image_path = os.path.join(cwd, "tests/unit_tests/media_test/barcode.png")
        cls.file_return = SimpleUploadedFile(
            name="barcode.png",
            content=open(image_path, "rb").read(),
            content_type="image/png",
        )

    @mock.patch(
        "datafetcher.oauthclient.oauth2api.oauth2api.get_application_token",
        side_effect=mocked_get_application_token,
    )
    @mock.patch(
        "datafetcher.oauthclient.credentialutil.credentialutil.load",
        side_effect=mocked_credential_load,
    )
    @mock.patch(
        "datafetcher.controllers.fetcher.requests.get", side_effect=mocked_requests_get
    )
    def test_gatherer_can_get_name_and_img_url(
        self, mocked_get_application_token, mocked_credential_load, mocked_requests_get
    ):
        gatherer = Gatherer(["5051889074847"])
        gatherer.get_name_and_img_url()
        self.assertEqual(
            gatherer.game_name, "Le Seigneur des anneaux - La guerre du Nord"
        )
        self.assertEqual(gatherer.get_avg_price(), 15)
