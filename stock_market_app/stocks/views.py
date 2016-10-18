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


def get_company_info(request):

    context_dict = {}

    response = render(request, 'stocks/company.html', context=context_dict)
    return response


def validate_data(day):
    '''
    :param day: A "day" object containing stock information (open, volume, high, low, close, and date)
    :return: True if data is valid
    '''
    if day['low'] > day['high']:
        print("low is greater than high")
        return False

    if day['open'] > day['high']:
        print("open is greater than high")
        return False

    if day['close'] > day['high']:
        print('close is greater than high')
        return False

    if day['open'] < day['low']:
        print('open is less than low')
        return False

    if day['close'] < day['low']:
        print('close is less than low')
        return False

    return True


def historical_pricing(request):

    context_dict = {}
    context_dict['form'] = HistoricalPricingForm()

    if request.method == 'POST':
        form = HistoricalPricingForm(request.POST)

        #Check form, gather information for API call
        if form.is_valid():
            symbol = form.cleaned_data['stock_symbol']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            interval = form.cleaned_data['interval']
            #print("{0},{1},{2},{3}".format(symbol,start_date,end_date,interval))


            try:
                #Make sure there isn't any previous data
                data = None
                graph = None
                context_dict['graph'] = None
                context_dict['data'] = None

                #API Call
                data = get_historical_pricing(symbol, start_date, end_date, interval)

                #print(data)

            except Exception as e:
                context_dict['err_message'] = e
                pass

            if data:
                if data['history'] != None:

                    #Gather all data in a list of objects containing stock information for a particular day.
                    symbol_data = []
                    for day in data['history']['day']:
                        if validate_data(day):
                            day_data = {'date': day['date'],
                                        'open': day['open'],
                                        'high': day['high'],
                                        'low': day['low'],
                                        'close': day['close'],}

                            symbol_data.append(day_data)

                        #For debugging
                        else:
                            print(day)

                    #Create candlestick chart using the data from symbol_data list created above
                    fig = FF.create_candlestick([day['open'] for day in symbol_data],
                                                [day['high'] for day in symbol_data],
                                                [day['low'] for day in symbol_data],
                                                [day['close'] for day in symbol_data],
                                                dates=[day['date'] for day in symbol_data])
                    fig['layout'].update({
                        'title': '{0} Historical Data'.format(symbol),
                        'yaxis': {'title': "Price in USD($)"},
                        'xaxis': {'title': "Date"},
                    })

                    #Graphically represent the data, send it to the page.
                    graph = opy.plot(fig, output_type='div', validate=False)
                    if graph:
                        context_dict['graph'] = graph

                    context_dict['form'] = form

                else:
                    context_dict['graph'] = None
                    context_dict['err_message'] = "History not available for this symbol"

    else:
        form = HistoricalPricingForm()


    return render(request, 'stocks/historical_pricing.html', context=context_dict)