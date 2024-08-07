# Generated by Django 5.0.2 on 2024-07-17 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('details', '0006_banner_cards'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='saved_doctors',
            field=models.ManyToManyField(related_name='saved_by_users', to='details.doctor'),
        ),
    ]
