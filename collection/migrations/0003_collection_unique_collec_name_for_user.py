# Generated by Django 4.1 on 2022-08-30 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0002_game_unique_barcode'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='collection',
            constraint=models.UniqueConstraint(fields=('name', 'user'), name='unique_collec_name_for_user'),
        ),
    ]