from django.conf.urls import url
from . import views

app_name = 'shop_app'

urlpatterns = [
    url(r'^$', views.List.as_view(), name='home'),
    url(r'^category/(?P<category_pk>[0-9]+)/$', views.List.as_view(), name='category'),
    url(r'^details/(?P<pk>[0-9]+)/$', views.Details.as_view(), name='details')
]
