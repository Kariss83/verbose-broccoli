""" This module adds the Collection and Games Models to the project
"""
# future
# standard library
# third-party
from djmoney.models.fields import MoneyField

# Django
from django.db import models

# local Django
from accounts.models import CustomUser


# Create your models here.
class Games(models.Model):
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

    def __str__(self):
        return self.name


class Collection(models.Model):
    """_summary_

    Args:
        models (_type_): _description_
    """
    name = models.CharField(max_length=50)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game = models.ManyToManyField(Games)

    def __str__(self):
        return self.name

    def _return_total_value(self):
        prices = []
        for game in self.game.all():
            prices.append(game.avg_price)
        return sum(prices)
