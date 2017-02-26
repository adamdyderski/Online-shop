from django.conf.urls import url
from . import views

app_name = 'cart'

urlpatterns = [
    url(r'^add/(?P<product_pk>[0-9]+)/$', views.addOrUpdate, name='add'),
    url(r'^update/(?P<product_pk>[0-9]+)/$', views.addOrUpdate, name='update'),
    url(r'^remove/(?P<product_pk>[0-9]+)/$', views.remove, name='remove'),
    url(r'^show/$', views.Show.as_view(), name='show')
]
