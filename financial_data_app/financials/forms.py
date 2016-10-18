from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime

class HistoricalPricingForm(forms.Form):
    stock_symbols = forms.CharField(required=True)

    start_date = forms.DateField(required=True,
                                 input_formats=['%Y-%m-%d'],
                                 widget=forms.SelectDateWidget(years=range(1980,2017)),
                                 initial=datetime.today())

    end_date = forms.DateField(required=True,
                               input_formats=['%Y-%m-%d'],
                               widget=forms.SelectDateWidget(years=range(1980,2017)),
                               initial=datetime.today())

    interval = forms.ChoiceField(choices=[('d', 'daily'),
                                          ('w', 'weekly'),
                                          ('m', 'monthly')])

    adjust_price = forms.BooleanField(required=False,
                                      widget=forms.CheckboxInput)


    def clean(self):
        data = self.cleaned_data
        data['stock_symbols'] = [x.strip() for x in data['stock_symbols'].split(',')]
        print(data['stock_symbols'])
        if data['start_date'] > data['end_date']:
            raise ValidationError('Start date should be before end date')
        if data['start_date'] == data['end_date']:
            raise ValidationError('Please select a range of more than one day')
        return data

class CompanySearchForm(forms.Form):
    search_query = forms.CharField(required=True)