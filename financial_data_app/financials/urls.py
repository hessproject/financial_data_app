from django.conf.urls import url
from financials import views

urlpatterns = [
    url(r'^$',
        views.index,
        name='index'),

    url(r'^financials/historical_pricing/$',
        views.historical_pricing,
        name='historical_pricing'),

    url(r'financials/company_search/$',
        views.company_search,
        name='company_search'),
]