from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from .signals import update_shares_list

class fx_table(models.Model):
    eur_to_gbp_pair = 'EUR/GBP'
    aud_to_gbp_pair = 'AUD/GBP'
    usd_to_gbp_pair = 'AUD/USD'

    eur_to_gbp = models.FloatField(default=0)
    aud_to_gbp = models.FloatField(default=0)
    usd_to_gbp = models.FloatField(default=0)

    date_time = models.DateTimeField(max_length=264,unique=True,default='')


class Cash(models.Model):
    reference = models.CharField(max_length=128)
    amount = models.FloatField(default=0)
    currency = models.CharField(max_length=128)

    def get_absolute_url(self):
        return reverse ('fx_rates_app:cash_list')


    def __str__(self):
        return self.reference


class Shares(models.Model):
    name = models.CharField(max_length=128,null=True)
    ticker = models.CharField(max_length=128,null=True)
    date = models.DateField(null=True)
    quantity = models.FloatField(default=0,null=True)
    price = models.FloatField(default=0,null=True)
    currency = models.CharField(max_length=128,null=True)
    current_price = models.FloatField(default=0,null=True)


    def get_absolute_url(self):
        return reverse ('fx_rates_app:shares_list')

    @property
    def book_value(self):
        book_val = self.quantity*self.price
        return book_val

    @property
    def market_value(self):
        market_val = self.quantity*self.current_price
        return market_val

    # @property
    # def market_value_gbp(self):
    #     latest_fx = fx_table.objects.last()
    #     if self.currency == 'AUD':
    #         total_share = self.current_price * self.quantity / latest_fx.aud_to_gbp
    #     elif self.currency == 'USD':
    #         total_share = self.current_price * self.quantity / latest_fx.usd_to_gbp
    #     elif self.currency == 'EUR':
    #         total_share = self.current_price * self.quantity / latest_fx.eur_to_gbp
    #     else:
    #         total_share = self.current_price * self.quantity
    #     return total_share

    # @property
    # def current_price(self):
    #     curr_price= self.ticker

post_save.connect(update_shares_list, sender=Shares)
