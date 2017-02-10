from django.conf.urls import url
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^registration/$', views.Registration.as_view(), name='registration')

]
