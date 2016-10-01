from django.conf.urls import url
from stocks import views

urlpatterns = [
    url(r'^$',
        views.index,
        name='index'),

    url(r'^stocks/$',
        views.stocks,
        name='stocks'),

    url(r'^profile/$',
        views.profile,
        name='profile'),

    url(r'^stocks/add_category/$',
        views.add_category,
        name='add_category')
]