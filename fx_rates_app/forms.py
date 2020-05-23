from django import forms
from fx_rates_app.models import Cash,Shares

MY_DATE_FORMATS = ['%d/%m/%Y',]

class CashForm(forms.ModelForm):
    class Meta():
        model = Cash
        fields = '__all__' #You want to be able to change all the fields


class SharesForm(forms.ModelForm):
    date = forms.DateField(input_formats=MY_DATE_FORMATS)
    class Meta():
        model = Shares
        fields = ('name','ticker','date','quantity','price','currency')
