# Generated by Django 5.0.4 on 2024-05-12 16:16

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0002_remove_booking_booking_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_time',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
