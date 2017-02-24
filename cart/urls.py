from django.conf.urls import url
from . import views

app_name = 'cart'

urlpatterns = [
    url(r'^add/(?P<product_pk>[0-9]+)/$', views.add, name='add'),
    url(r'^show/$', views.Show.as_view(), name='show')
]
