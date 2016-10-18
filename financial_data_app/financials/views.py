from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from financials.forms import HistoricalPricingForm, CompanySearchForm
from financials import symbol_data, tradier
from registration.views import RegistrationView
from plotly import offline as opy
from plotly.graph_objs import *
from plotly.tools import FigureFactory as FF

# Create your views here.
def index(request):

    context_dict = {}

    response = render(request, 'financials/index.html', context=context_dict)
    return response


def historical_pricing(request):

    context_dict = {}
    context_dict['form'] = HistoricalPricingForm
    context_dict['graphs'] = []

    if request.method == "POST":
        form = HistoricalPricingForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            stock_symbols = form_data['stock_symbols']
            start_date = form_data['start_date']
            end_date = form_data['end_date']
            interval = form_data['interval']
            adjust_price = form_data['adjust_price']

            #Fetch stock data
            data = symbol_data.get_stock_data(stock_symbols, start=start_date, end=end_date, interval=interval, adjust_price=adjust_price)
            print(data)

            #Create graph from collected data
            for symbol in data:
                ticker = data[symbol]

                #The actual graph content
                fig = FF.create_candlestick(ticker.Open, ticker.High, ticker.Low, ticker.Close, dates=ticker.index)

                #Adding titles to the graph and axes
                fig['layout'].update({
                    'title': '{0} Historical Price'.format(symbol),
                    'yaxis': {'title': 'Price in USD($)'},
                    'xaxis': {'title': 'Dates'}
                })

                #Adding an "Adjusted Close" line, not available if the data is already adjusted
                if not adjust_price:
                    adj_close_line = Scatter(
                        x=ticker.index,
                        y=ticker['Adj Close'],
                        name="Adjusted Close",
                        line=Line(color='black')
                    )

                    fig['data'].extend([adj_close_line])

                #Plot the graph, and add the divs to the context_dict to be passed to the page
                graph = opy.plot(fig, validate=False, output_type='div')
                context_dict['graphs'].append(graph)


    return render(request, 'financials/historical_pricing.html', context=context_dict)


def company_search(request):
    context_dict = {}
    context_dict['form'] = CompanySearchForm
    context_dict['err_message'] = None
    context_dict['results'] = None

    if request.method == 'POST':

        form = CompanySearchForm(request.POST)

        if form.is_valid():

            #Clean the query
            form_data = form.cleaned_data
            query = form_data['search_query'].strip()

            #Query the Tradier API
            results = tradier.get_company_info(query)

            #Return top ten results (sorted by average volume)
            if results['securities'] is not None:
                context_dict['results'] = results['securities']['security'][:10]
            else:
                context_dict['err_message'] = "No results found or invalid query"


    return render(request, 'financials/company_search.html', context=context_dict)
