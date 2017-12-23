from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^films/(?P<film_id>\d*)$', views.film_view, name='film_view'),
    url(r'^halls/(?P<hall_id>\d*)$', views.hall_view, name='hall_view'),
    url(r'^seances/(?P<seance_id>\d*)$', views.seance_view, name='seance_view'),
    url(r'^tickets/(?P<ticket_id>\d*)$', views.ticket_view, name='ticket_view'),
]