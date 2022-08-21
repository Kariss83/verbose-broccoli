"""

"""
from djmoney.models.fields import MoneyField
from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Games(models.Model):
    """_summary_

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    image = models.URLField(max_length=255)
    avg_price = MoneyField(max_digits=14,
                           decimal_places=2,
                           default_currency='USD')
    barcode = models.CharField(max_length=50)
    platform = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Table de jonction pour les catégories
class Collection(models.Model):
    """_summary_

    Args:
        models (_type_): _description_
    """
    name = models.CharField(max_length=50)
    total_value = MoneyField(max_digits=14,
                           decimal_places=2,
                           default_currency='USD')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game = models.ManyToManyField(Games)