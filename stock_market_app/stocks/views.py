from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from stocks.forms import HistoricalPricingForm
from stocks.tradier import get_historical_pricing, find_company
from registration.views import RegistrationView
from plotly import offline as opy
from plotly import graph_objs as go
from plotly.tools import FigureFactory as FF

# Create your views here.
def index(request):

    context_dict = {}

    response = render(request, 'stocks/index.html', context=context_dict)
    return response


def show_stock(request):

    context_dict = {}

    response = render(request, 'stocks/stock.html', context=context_dict)
    return response


@staff_member_required
def add_category(request):

    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)

    context_dict = {'form': form, }

    return render(request, 'stocks/add_category.html', context_dict)


def stocks(request):

    context_dict = {}
    return render(request, 'stocks/stocks.html', context=context_dict)


def profile(request):

    context_dict = {}
    return render(request, 'stocks/profile.html', context=context_dict)


def historical_pricing(request):
    context_dict = {}
    context_dict['data'] = None
    context_dict['graph'] = None
    context_dict['form'] = HistoricalPricingForm()
    data = None
    graph = None

    if request.method == 'POST':
        form = HistoricalPricingForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['stock_symbol']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            interval = form.cleaned_data['interval']

        try:
            data = get_historical_pricing(symbol, start_date, end_date, interval)
            context_dict['data'] = data
            print(data)
        except Exception as e:
            print("Error: " + e)
            context_dict['err_message'] = "No data for this symbol or error connecting to Tradier API"

    else:
        form = HistoricalPricingForm()

    if data:
        dates = []
        highs = []
        lows = []
        opens = []
        closes = []
        for day in data['history']['day']:
            dates.append(day['date'])
            opens.append(day['open'])
            highs.append(day['high'])
            lows.append(day['low'])
            closes.append(day['close'])

        fig = FF.create_candlestick(opens, highs, lows, closes, dates=dates)

        graph = opy.plot(fig, output_type='div', validate=False)
        if graph:
            context_dict['graph'] = graph

        context_dict['form'] = form

    return render(request, 'stocks/historical_pricing.html', context=context_dict)