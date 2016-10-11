from django import forms

class HistoricalPricingForm(forms.Form):
    stock_symbol = forms.CharField(required=True, max_length=5,
                           help_text='Stock Symbol')
    start_date = forms.DateField(required=True, input_formats=['%Y-%m-%d'], widget=forms.SelectDateWidget, help_text='Start Date')
    end_date = forms.DateField(required=True, input_formats=['%Y-%m-%d'], widget=forms.SelectDateWidget, help_text='End Date')
    interval = forms.ChoiceField(help_text='Time Interval',choices=[('daily', 'daily'),
                                          ('weekly', 'weekly'),
                                          ('weekly', 'monthly')] )

    def clean(self):
        data = self.cleaned_data
        if data['start_date'] > data['end_date']:
            raise ValidationError('Start date should be before end date')
        if data['start_date'] == data['end_date']:
            raise ValidationError('Please select a range of more than one day')
        return data