from django.conf.urls import url
from . import views

app_name = 'shop_app'

urlpatterns = [
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^details/(?P<pk>[0-9]+)/$', views.ProductDetails.as_view(), name='details')
]
