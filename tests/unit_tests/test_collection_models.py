from djmoney.money import Money

from django.test import TestCase

from gamezscan.accounts.models import CustomUser
from gamezscan.collection.models import Collection, Game


def create_an_user(number):
    user_test = CustomUser.objects.create(
        email=f"test{number}@gmail.com", username=f"MRTest{number}"
    )
    return user_test


def create_a_game(name, avg_price, barcode):
    game = Game.objects.create(name=f"test{name}", avg_price=avg_price, barcode=barcode)
    return game


def create_a_collection(name, user):
    collection = Collection.objects.create(name=f"test{name}", user=user)
    return collection


def add_game_to_collection(collection, games_to_add):
    """Add a given game to a given collection

    Args:
        collection (model): A set of games related to a given user
        games_to_add (list or tuple): list or tuple of games to add
                                      to the collection
    """
    collection.games.add(games_to_add)


class TestDatafetcher(TestCase):
    """This class holds all the tests for Datafetcher

    Args:
        TestCase (class): Django's default test class
    """

    @classmethod
    def setUpTestData(cls):
        """Setting up data for testing"""
        cls.user = create_an_user(1)

        cls.gameLOTR = create_a_game(
            "Le Seigneur des anneaux - La guerre du Nord", 14, 5051889074847
        )
        cls.game1 = create_a_game(1, 10, 505051889074846)
        cls.game2 = create_a_game(2, 30, 505051889074845)
        cls.game3 = create_a_game(3, 20, 505051889074844)

        cls.collection = create_a_collection("mycollection", cls.user)
        # Adding games to the collection
        cls.collection.games.add(cls.gameLOTR, cls.game1, cls.game2)

    def test_Game_return_correct_name(self):
        name = self.gameLOTR.__str__()
        self.assertEqual(name, "testLe Seigneur des anneaux - La guerre du Nord")

    def test_Collection_return_correct_name(self):
        name = self.collection.__str__()
        self.assertEqual(name, "testmycollection")

    def test_collection_can_return_total_value(self):
        value = self.collection._return_total_value()
        self.assertEqual(value, Money("54.00", "USD"))
