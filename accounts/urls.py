from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'accounts'

urlpatterns = [

    # Rejestracja
    url(r'^activate/(?P<activation_key>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', views.activate, name='activate'),
    url(r'^registration/$', views.UserRegistration.as_view(), name='registration'),

    # Profil użytkownika
    url(r'^profile/$', login_required(views.UserUpdate.as_view()), name='profile'),

    # Zamówienia
    url(r'^orders/$', login_required(views.MyOrders.as_view()), name='orders'),
]
