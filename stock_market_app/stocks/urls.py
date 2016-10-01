from django.conf.urls import url
from stocks import views

urlpatterns = [
    url(r'^$',
        views.index,
        name='index'),

]