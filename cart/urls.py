from django.conf.urls import url
from . import views

app_name = 'cart'

urlpatterns = [
    url(r'^add/(?P<product_pk>[0-9]+)/$', views.add_or_update, name='add'),
    url(r'^update/(?P<product_pk>[0-9]+)/$', views.add_or_update, name='update'),
    url(r'^remove/(?P<product_pk>[0-9]+)/$', views.remove, name='remove'),
    url(r'^set/shippingmethod/$', views.set_shipping_method, name='shipping_method'),
    url(r'^show/$', views.ShowCart.as_view(), name='show'),
    url(r'^order/create/$', views.order_create, name='order_create')
]
