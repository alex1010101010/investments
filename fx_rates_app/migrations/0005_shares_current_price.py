# Generated by Django 2.2.5 on 2020-04-20 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fx_rates_app', '0004_remove_cash_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='shares',
            name='current_price',
            field=models.FloatField(default=0),
        ),
    ]
