""" This module adds the Collection and Game Models to the project
"""
# future
# standard library
# third-party
from djmoney.models.fields import MoneyField

# Django
from django.urls import reverse
from django.db import models

# local Django
from accounts.models import CustomUser


# Create your models here.
class Game(models.Model):
    """_summary_

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    PLATFORM_CHOICES = [
        ('PC', 'PC'),
        ('XBOX', 'XBOX'),
        ('XBOX360', 'XBOX360'),
        ('XBOX1', 'XBOX One'),
        ('PS1', 'Playstation 1'),
        ('PS2', 'Playstation 2'),
        ('PS3', 'Playstation 3'),
        ('PS4', 'Playstation 5'),
        ('PS6', 'Playstation 6'),
        ('SWITCH', 'Nintendo Switch'),
        ('GB', 'Game Boy'),
        ('ND', 'Unknown')
    ]
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    image = models.URLField(max_length=255)
    avg_price = MoneyField(max_digits=14,
                           decimal_places=2,
                           default_currency='USD')
    barcode = models.CharField(max_length=50)
    platform = models.CharField(max_length=50,
                                choices=PLATFORM_CHOICES,
                                default='ND',
                                blank=False
                                )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['barcode'], name="unique_barcode")
            ]

    def get_absolute_url(self):
        return reverse("collection:game_detail", kwargs={"barcode": self.barcode})

    def __str__(self):
        return self.name


class Collection(models.Model):
    """_summary_

    Args:
        models (_type_): _description_
    """
    name = models.CharField(max_length=50)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    games = models.ManyToManyField(Game)

    def __str__(self):
        return self.name

    def _return_total_value(self):
        prices = []
        for game in self.games.all():
            prices.append(game.avg_price)
        return sum(prices)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'user'], name="unique_collec_name_for_user")
            ]
