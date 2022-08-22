# Generated by Django 4.1 on 2022-08-22 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0002_remove_collection_game_collection_game'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='total_value',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='total_value_currency',
        ),
        migrations.AddField(
            model_name='games',
            name='platform',
            field=models.CharField(choices=[('PC', 'PC'), ('XBOX', 'XBOX'), ('XBOX360', 'XBOX360'), ('XBOX1', 'XBOX One'), ('PS1', 'Playstation 1'), ('PS2', 'Playstation 2'), ('PS3', 'Playstation 3'), ('PS4', 'Playstation 5'), ('PS6', 'Playstation 6'), ('SWITCH', 'Nintendo Switch'), ('GB', 'Game Boy'), ('ND', 'Unknown')], default='ND', max_length=50),
        ),
    ]
