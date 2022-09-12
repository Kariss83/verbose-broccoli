from unittest import mock
from datetime import datetime, timedelta

from django.test import TestCase

from gamezscan.datafetcher import constants
from gamezscan.datafetcher.controllers import fetcher
from gamezscan.datafetcher.oauthclient.model.model import oAuth_token


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if "https://product-lookup-by-upc-or-ean.p.rapidapi.com/code/" in args[0]:
        return MockResponse(constants.EAN_API_RETURN, 200)
    elif args[0] == "https://api.ebay.com/buy/browse/v1/item_summary/search?":
        return MockResponse(constants.EBAY_RETURN, 200)

    return MockResponse(None, 404)


def mocked_get_application_token(*args, **kwargs):
    token = oAuth_token()
    token.access_token = "myfaketoken"
    token.token_expiry = datetime.utcnow() + timedelta(hours=5) - timedelta(minutes=5)
    return token


def mocked_credential_load(*args, **kwargs):
    pass


class TestDatafetcher(TestCase):
    """This class holds all the tests for Datafetcher

    Args:
        TestCase (class): Django's default test class
    """

    @mock.patch(
        "gamezscan.datafetcher.controllers.fetcher.requests.get", side_effect=mocked_requests_get
    )
    def test_can_retrieve_game_name_using_ean(self, mocked_requests_get):
        communicator = fetcher.EANAPICommunicator()
        result = communicator.request_ean_lookup(5051889074847)
        self.assertEqual(
            result["product"]["name"], "Le Seigneur des anneaux - La guerre du Nord"
        )

    @mock.patch(
        "gamezscan.datafetcher.oauthclient.oauth2api.oauth2api.get_application_token",
        side_effect=mocked_get_application_token,
    )
    @mock.patch(
        "gamezscan.datafetcher.oauthclient.credentialutil.credentialutil.load",
        side_effect=mocked_credential_load,
    )
    @mock.patch(
        "gamezscan.datafetcher.controllers.fetcher.requests.get", side_effect=mocked_requests_get
    )
    def test_can_retrieve_avg_price_on_ebay(
        self, mocked_get_application_token, mocked_credential_load, mocked_requests_get
    ):
        communicator = fetcher.EBAYCommunicator(
            "The lord of the rings : War in the north"
        )
        communicator.request_info()
        avg_price = communicator.get_avg_price()
        self.assertEqual(avg_price, 15)
