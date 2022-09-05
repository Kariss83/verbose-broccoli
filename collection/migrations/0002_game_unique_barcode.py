# Generated by Django 4.1 on 2022-08-29 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='game',
            constraint=models.UniqueConstraint(fields=('barcode',), name='unique_barcode'),
        ),
    ]
