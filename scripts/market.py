import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','fx_rates_project.settings')

import django
django.setup()


from fx_rates_app.models import Shares

from pandas_datareader import yahoo
import yfinance as yf
import pandas_datareader.data as web
from datetime import datetime

def run(ticker):
    new_price = yahoo.quotes.YahooQuotesReader(ticker).read()['price']
    pg1, created = Shares.objects.get_or_create(ticker=ticker)
    pg1.current_price = new_price
    pg1.save()
    print('hi')
    return pg1
