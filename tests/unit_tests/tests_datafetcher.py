from unittest import mock

from django.test import TestCase

from datafetcher import constants
from datafetcher.controllers import fetcher
from accounts.models import CustomUser
from collection.models import Collection, Game


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if 'https://product-lookup-by-upc-or-ean.p.rapidapi.com/code/' in args[0]:
        return MockResponse(constants.EAN_API_RETURN, 200)
    elif args[0] == 'https://api.ebay.com/buy/browse/v1/item_summary/search?':
        return MockResponse(constants.EBAY_RETURN, 200)

    return MockResponse(None, 404)


def create_an_user(number):
    user_test = CustomUser.objects.create(
            email=f"test{number}@gmail.com",
            username=f"MRTest{number}"
        )
    return user_test


def create_a_game(name, avg_price, barcode):
    game = Game.objects.create(
            name=f"test{name}",
            avg_price=avg_price,
            barcode=barcode
            )
    return game


def create_a_collection(name, user):
    collection = Collection.objects.create(
            name=f"test{name}collection",
            user=user
            )
    return collection


def add_game_to_collection(collection, games_to_add):
    """ Add a given game to a given collection

    Args:
        collection (model): A set of games related to a given user
        games_to_add (list or tuple): list or tuple of games to add
                                      to the collection
    """
    collection.games.add(games_to_add)


class TestDatafetcher(TestCase):
    """ This class holds all the tests for Datafetcher

    Args:
        TestCase (class): Django's default test class
    """
    @classmethod
    def setUpTestData(cls):
        """Setting up data for testing
        """
        cls.user = create_an_user(1)

        cls.gameLOTR = create_a_game("Le Seigneur des anneaux - La guerre du Nord",
                                     14,
                                     5051889074847)
        cls.game1 = create_a_game(1, 10, 505051889074846)
        cls.game2 = create_a_game(2, 30, 505051889074845)
        cls.game3 = create_a_game(3, 20, 505051889074844)

        cls.collection = create_a_collection("mycollection", cls.user)
        # Adding games to the collection
        cls.collection.games.add(cls.gameLOTR, cls.game1, cls.game2)

    @mock.patch('datafetcher.controllers.fetcher.requests.get', side_effect=mocked_requests_get)
    def test_can_retrieve_game_name_using_ean(self, mocked_requests_get):
        communicator = fetcher.EANAPICommunicator()
        result = communicator.request_ean_lookup(5051889074847)
        self.assertEqual(result['product']['name'], 'Le Seigneur des anneaux - La guerre du Nord')

    @mock.patch('datafetcher.controllers.fetcher.requests.get', side_effect=mocked_requests_get)
    def test_can_retrieve_avg_price_on_ebay(self, mocked_requests_get):
        communicator = fetcher.EBAYCommunicator("The lord of the rings : War in the north")
        communicator.request_info()
        # import pdb; pdb.set_trace()
        avg_price = communicator.get_avg_price()
        self.assertEqual(avg_price, 15)
