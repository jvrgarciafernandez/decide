# Generated by Django 2.0 on 2020-01-12 22:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0003_auto_20180605_0842'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionoption',
            name='dhont',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='questionoption',
            name='numero_dhont',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]
