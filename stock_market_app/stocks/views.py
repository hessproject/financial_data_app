from django.shortcuts import render

# Create your views here.
def index(request):

    context_dict = {}

    response = render(request, 'stocks/index.html', context=context_dict)
    return response

def show_stock(request):

    context_dict = {}

    response = render(request, 'stocks/stock.html', context=context_dict)
    return response