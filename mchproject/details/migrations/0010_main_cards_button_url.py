# Generated by Django 5.0.2 on 2024-08-06 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0009_banner_cards_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='main_cards',
            name='button_url',
            field=models.URLField(default='/doctor'),
        ),
    ]