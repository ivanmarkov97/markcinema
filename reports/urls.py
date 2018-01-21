from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^profit_film/$', views.profit_film_view, name='profit_film_view'),
    url(r'^profit_seance/$', views.profit_seance_view, name='profit_seance_view'),
]