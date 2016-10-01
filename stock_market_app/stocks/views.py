from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from stocks.models import Category
from stocks.forms import CategoryForm
from registration.views import RegistrationView

# Create your views here.
def index(request):

    category_list = Category.objects.all()

    context_dict = {'market_data_list': category_list}

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