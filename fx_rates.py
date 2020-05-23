import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','fx_rates_project.settings')

import django
# Import settings
django.setup()


from fx_rates_app.models import fx_table

import pandas_datareader.data as web
from datetime import datetime

def main():
    os.environ["ALPHAVANTAGE_API_KEY"] = 'XXXXXXXX'
    fx_gbp_to_eur = web.DataReader("GBP/EUR","av-forex")
    eur = float(fx_gbp_to_eur[4:5].values[0][0])


    fx_gbp_to_aud = web.DataReader("GBP/AUD","av-forex")
    aud = float(fx_gbp_to_aud[4:5].values[0][0])


    fx_gbp_to_usd = web.DataReader("GBP/USD","av-forex")
    usd = float(fx_gbp_to_usd[4:5].values[0][0])


    # Get date and time
    from datetime import datetime

    # datetime object containing current date and time
    now = datetime.now()


    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")


    # we populate the model fx_table with the data from the Python script
    webpg1 = fx_table.objects.get_or_create(eur_to_gbp=eur,aud_to_gbp=aud,usd_to_gbp=usd,date_time=dt_string)[0]

    return webpg1


if __name__ == '__main__':
    main()
