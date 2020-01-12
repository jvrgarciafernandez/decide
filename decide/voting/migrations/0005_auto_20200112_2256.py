# Generated by Django 2.0 on 2020-01-12 22:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0004_auto_20200112_2252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionoption',
            name='dhont',
        ),
        migrations.RemoveField(
            model_name='questionoption',
            name='numero_dhont',
        ),
        migrations.AddField(
            model_name='voting',
            name='dhont',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='voting',
            name='numero_dhont',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]