from django.contrib import admin
from fx_rates_app.models import fx_table,Cash,Shares




admin.site.register(fx_table)
admin.site.register(Cash)
admin.site.register(Shares)
