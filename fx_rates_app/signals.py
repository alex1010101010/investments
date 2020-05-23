from pandas_datareader import yahoo

def update_shares_list(sender, **kwargs):
    if kwargs.get('created', False):
        share = kwargs.get('instance')
        new_price = yahoo.quotes.YahooQuotesReader(share.ticker).read()['price']
        share.current_price = new_price
        share.save()