from django import forms
import csv

class StockTickerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(StockTickerForm, self).__init__(*args, **kwargs)
        self.fields['ticker'] = forms.ChoiceField(
            choices = self.get_ticker_choices(),
            widget = forms.Select(attrs={
                'class': 'form-select', 
                'style': 'width: 500px; max-height: 150px; overflow-y: auto; margin-right: 10px;'})
            )

    def get_ticker_choices(self):
        ticker_choices = []
        with open('stocks/tickers.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                symbol = row[0]
                company = row[1]
                ticker_choices.append((symbol, f"{symbol} - {company}"))
        return ticker_choices
