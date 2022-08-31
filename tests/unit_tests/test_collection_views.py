"""This module is designed to host all the unit tests for the views of
the part of the program in charge of scanning and reading barcodes.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import PermissionDenied


from collection.models import Game, Collection
from accounts.models import CustomUser

def create_a_game(name, avg_price, barcode):
    game = Game.objects.create(
            name=f"test{name}",
            avg_price=avg_price,
            barcode=barcode
            )
    return game


def create_a_collection(name, user):
    collection = Collection.objects.create(
            name=f"test{name}",
            user=user
            )
    return collection


class TestCollectionViewsModule(TestCase):
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
        cls.user.set_password('monsupermotdepasse')
        cls.user.save()
        
        cls.first_collection = Collection.objects.create(
            name='My First Collection',
            user=cls.user
        )

        cls.gameLOTR = create_a_game(
            "Le Seigneur des anneaux - La guerre du Nord",
            14,
            5051889074847
        )
        cls.game1 = create_a_game(1, 10, 505051889074846)
        cls.game2 = create_a_game(2, 30, 505051889074845)
        cls.game3 = create_a_game(3, 20, 505051889074844)

        # Adding games to the collection
        cls.first_collection.games.add(cls.game1)

        cls.all_collections_url = reverse('collection:all_collections')
        cls.add_game_to_collection_url = reverse('collection:add_game_to_collection')
        cls.create_collection_url = reverse('collection:create')

    def test_add_game_to_collection_GET(self):
        self.client.login(email='test@gmail.com', password='monsupermotdepasse')
        response = self.client.get(self.add_game_to_collection_url)
        self.assertRaises(PermissionDenied)
    
    def test_add_game_to_collection_POST(self):
        self.client.login(email='test@gmail.com', password='monsupermotdepasse')
        response = self.client.post(
            self.add_game_to_collection_url,
            {'collections': 'My First Collection',
            'barcode': '5051889074847', 
            },
            follow=True
        )
        collection = Collection.objects.get(name='My First Collection', user=self.user)
        game_list = [game for game in collection.games.all()]
        self.assertEqual(str(self.gameLOTR.name), str(game_list[0]))

    def test_see_all_collections_GET(self):
        self.client.login(email='test@gmail.com', password='monsupermotdepasse')
        response = self.client.get(self.all_collections_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'collections/all_collections.html')
    
    def test_create_new_collection_GET(self):
        self.client.login(email='test@gmail.com', password='monsupermotdepasse')
        response = self.client.get(self.create_collection_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'collections/create_new.html')
    
    def test_create_new_collection_POST(self):
        self.client.login(email='test@gmail.com', password='monsupermotdepasse')
        response = self.client.post(
            self.create_collection_url,
            {'name': 'My Second Collection'},
            follow=True
        )
        collections = Collection.objects.filter(user = self.user)
        self.assertTrue(len(collections) == 2)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'collections/all_collections.html')
    
    def test_create_new_collection_POST_integrity_error(self):
        self.client.login(email='test@gmail.com', password='monsupermotdepasse')
        response = self.client.post(
            self.create_collection_url,
            {'name': 'My First Collection'},
            follow=True
        )
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertTrue('You already have a collection with that name' in str(messages[0]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'collections/create_new.html')


    