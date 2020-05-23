from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.http import require_http_methods
from fx_rates_app.forms import SharesForm,CashForm
from django.views.generic import TemplateView,ListView,CreateView,DetailView,UpdateView,DeleteView
from django.urls import reverse
from fx_rates_app import forms
from fx_rates_app.models import Cash, Shares,fx_table
import datetime
from django.db.models import Sum, When, Case, FloatField, Value, F,Max,Q
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
import fx_rates as update
from django.urls import reverse_lazy
from django.utils import timezone
from fx_rates_app.models import Shares
from subprocess import call
from pandas_datareader import yahoo
import yfinance as yf
import pandas_datareader.data as web
from datetime import datetime
import pdb

class index(TemplateView):
    template_name = 'fx_rates_app/index.html'
    def get_context_data(self,**kwargs):
        context  = super().get_context_data(**kwargs)
        latest_fx = fx_table.objects.last()
        total_cash_book = Cash.objects.annotate(amount_in_gbp=Case(
                When(currency="AUD", then=F('amount')/latest_fx.aud_to_gbp),
                When(currency="USD", then=F('amount')/latest_fx.usd_to_gbp),
                When(currency="EUR", then=F('amount')/latest_fx.eur_to_gbp),
                default=F('amount'),
                output_field=FloatField()
            )
        ).aggregate(sum=Sum('amount_in_gbp'))['sum']
        total_share_book = Shares.objects.annotate(amount_in_gbp=Case(
                When(currency="AUD", then=F('price')*F('quantity')/latest_fx.aud_to_gbp),
                When(currency="USD", then=F('price')*F('quantity')/latest_fx.usd_to_gbp),
                When(currency="EUR", then=F('price')*F('quantity')/latest_fx.eur_to_gbp),
                default=F('price')*F('quantity'),
                output_field=FloatField()
            )
        ).aggregate(sum=Sum('amount_in_gbp'))['sum']

        total_share_mark = Shares.objects.annotate(each_mark=Case(
                When(currency="AUD", then=F('current_price')*F('quantity')/latest_fx.aud_to_gbp),
                When(currency="USD", then=F('current_price')*F('quantity')/latest_fx.usd_to_gbp),
                When(currency="EUR", then=F('current_price')*F('quantity')/latest_fx.eur_to_gbp),
                default=F('current_price')*F('quantity'),
                output_field=FloatField()
            )
        ).aggregate(sum=Sum('each_mark'))['sum']
        total_share_book = total_share_book or 0
        total_share_mark = total_share_mark or 0
        total_cash_book = total_cash_book or 0
        context['total_book'] = total_cash_book + total_share_book
        context['total_mark'] = total_cash_book + total_share_mark
        context['gain_loss'] = (total_cash_book + total_share_mark)-(total_cash_book + total_share_book)
        return context

# This is a test function
# class CView(View):
#     def get(self,request):
#         return HttpResponse("This doesn't need an html page")

class CashListView(ListView):
    model = Cash
    context_object_name = 'cash_details'

    def get_context_data(self, **kwargs):
        context = super(CashListView, self).get_context_data(**kwargs)
        latest_fx = fx_table.objects.last()
        queryset = self.get_queryset().annotate(cash_pos_gbp=Case(
                When(currency="AUD", then=F('amount')/latest_fx.aud_to_gbp),
                When(currency="USD", then=F('amount')/latest_fx.usd_to_gbp),
                When(currency="EUR", then=F('amount')/latest_fx.eur_to_gbp),
                default=F('amount'),
                output_field=FloatField()
            )
        )
        context['cash_details'] = queryset
        context['total_cash'] = queryset.aggregate(sum=Sum('cash_pos_gbp'))['sum']
        return context

##################################################################
# Shares

class SharesListView(ListView):
    model = Shares
    context_object_name = 'shares_details'

    # def update2(self):
    #     try:
    #         _ = update2.main()
    #     except:
    #         pass
    #     return redirect('/fx_rates_app/shares_list/')

    def get_queryset(self):
        return Shares.objects.all().order_by('-date')


    def get_context_data(self, **kwargs):
        context = super(SharesListView, self).get_context_data(**kwargs)
        latest_fx = fx_table.objects.last()
        queryset = self.get_queryset().annotate(
            stock_book_gbp=Case(
                When(currency="AUD", then=F('price')*F('quantity')/latest_fx.aud_to_gbp),
                When(currency="USD", then=F('price')*F('quantity')/latest_fx.usd_to_gbp),
                When(currency="EUR", then=F('price')*F('quantity')/latest_fx.eur_to_gbp),
                default=F('price')*F('quantity'),
                output_field=FloatField()
            ),
            stock_mark_gbp=Case(
                When(currency="AUD", then=F('current_price') * F('quantity') / latest_fx.aud_to_gbp),
                When(currency="USD", then=F('current_price') * F('quantity') / latest_fx.usd_to_gbp),
                When(currency="EUR", then=F('current_price') * F('quantity') / latest_fx.eur_to_gbp),
                default=F('current_price') * F('quantity'),
                output_field=FloatField()
            )
        # )
        # total_share = Shares.objects.annotate(stock_mark_gbp=Case(
        #     When(currency="AUD", then=F('current_price') * F('quantity') / latest_fx.aud_to_gbp),
        #     When(currency="USD", then=F('current_price') * F('quantity') / latest_fx.usd_to_gbp),
        #     When(currency="EUR", then=F('current_price') * F('quantity') / latest_fx.eur_to_gbp),
        #     default=F('current_price') * F('quantity'),
        #     output_field=FloatField()
        # )
        )
        # context['market_share_details'] = total_share

        context['shares_details'] = queryset
        context['tot_mark_gbp'] = queryset.aggregate(sum=Sum('stock_mark_gbp'))['sum']
        context['tot_book_gbp'] = queryset.aggregate(sum=Sum('stock_book_gbp'))['sum']
        return context


class FxListView(ListView):
    model = fx_table

    def get_queryset(self):
        return fx_table.objects.all().order_by('-date_time')
        # return fx_table.objects.last() why can't I use this?


    def update(self):
        try:
            _ = update.main()
        except:
            pass
        return redirect('/fx_rates_app/fx_list/')

##################################################################
#I want to includes Views for updating and deleting stuff
#For cash

class CashDetailView(DetailView):
    context_object_name = 'cash_detail'
    model = models.Cash
    template_name = 'fx_rates_app/cash_detail.html'

class CashUpdateView(UpdateView):
    fields = ('reference','amount','currency')
    model = models.Cash

class CashDeleteView(DeleteView):
    model = models.Cash
    success_url = reverse_lazy ('fx_rates_app:cash_list')

class CashCreateView(CreateView,LoginRequiredMixin):
    login_url ='/login/'
    redirect_field_name = 'fx_rates_app/cash_list.html'
    form_class = CashForm
    model = models.Cash


##################################################################
#For shares

class SharesDetailView(DetailView):
    context_object_name = 'shares_detail'
    model = models.Shares
    template_name = 'fx_rates_app/shares_detail.html'

class SharesUpdateView(UpdateView):
    fields = ('name','ticker','date','quantity','price','currency','current_price')
    model = models.Shares

class SharesDeleteView(DeleteView):
    model = models.Shares
    success_url = reverse_lazy ('fx_rates_app:shares_list')

class SharesCreateView(CreateView,LoginRequiredMixin):
    login_url ='/login/'
    redirect_field_name = 'fx_rates_app/shares_list.html'
    form_class = SharesForm
    model = models.Shares


# How can we do this using CBVs?
@require_http_methods("POST")
def update_shares_list(request):
    print('test')
    shares = Shares.objects.all()
    for share in shares:
        new_price = yahoo.quotes.YahooQuotesReader(share.ticker).read()['price']
        share.current_price = new_price
        share.save()
    print('hello')
    return redirect('/fx_rates_app/shares_list/')
