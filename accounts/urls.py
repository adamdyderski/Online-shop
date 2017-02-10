from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [

    # Rejestracja

    url(r'^activate/(?P<activation_key>[a-z0-9]+)/$', views.activate, name='activate'),
    url(r'^registration/$', views.Registration.as_view(), name='registration'),
    
    # Logowanie

    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout_then_login, name='logout'),

    # Reset hasła

    url(r'^password_reset/$', auth_views.password_reset, {'template_name' : 'accounts/reset/password_reset_form.html', 'post_reset_redirect' : '/accounts/password_reset/done/', 'email_template_name' : 'accounts/reset/password_reset_email.html', 'html_email_template_name' : 'accounts/reset/password_email.html'}, name="password_reset"),
    url(r'^password_reset/done/$', auth_views.password_reset_done, {'template_name' : 'accounts/reset/password_reset_done.html'}),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, {'template_name' : 'accounts/reset/password_reset_confirm.html','post_reset_redirect' : '/accounts/reset/done/'}, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete ,{'template_name' : 'accounts/reset/password_reset_complete.html'}),

    # Zmiana hasła

    url(r'^password_change/$', auth_views.password_change,{'template_name' : 'accounts/change/password_change_form.html','post_change_redirect' : '/accounts/password_change/done/'}, name='password_change'),
    url(r'^password_change/done/$', auth_views.password_change_done,{'template_name' : 'accounts/change/password_change_done.html'}, name='password_change_done'),

]
