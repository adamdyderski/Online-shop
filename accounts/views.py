from django.contrib import messages

from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic.edit import UpdateView, View
from django.views.generic import TemplateView

from accounts.forms import RegistrationFrom
from accounts.models import User
from cart.models import Order, OrderProduct


class UserUpdate(SuccessMessageMixin, UpdateView):
    model = User
    fields = ['first_name','last_name', 'street', 'postcode', 'city', 'email' ,'phone']
    template_name_suffix = '_update_form'
    success_message = 'Twoje dane zostały zaktualizowane!'

    def get_object(self, queryset=None):
        return self.request.user


def activate(request, activation_key):
    try:
        user = User.objects.get(activation_key=activation_key)
    except ObjectDoesNotExist:
        messages.error(request, 'Wystąpił problem! Spróbuj ponownie później lub skontaktuj się z nami.')
    else:
        if user.is_active:
            messages.info(request, 'Twoje konto jest już aktywne!')
        else:
            user.is_active = True
            user.save()
            messages.success(request, 'Gratulacje, Twoje konto zostało aktywowane!')

    return HttpResponseRedirect('/accounts/login')


class UserRegistration(View):
    template_name = 'accounts/user_registration_form.html'

    def get(self, request, *args, **kwargs):
        form = RegistrationFrom()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegistrationFrom(request.POST)

        if form.is_valid():
            user = form.save()
            html_message = render_to_string(
                'accounts/activation_email.html', {'activation_key': user.activation_key})
            user.email_user('Aktywacja konta', '', html_message=html_message)
            messages.success(
                request, 'Rejestracja przebiegła pomyślnie! Odbierz teraz waidomość wysłaną na podany adres email, aby aktywować swoje konto!')
            return HttpResponseRedirect('/accounts/login')

        return render(request, self.template_name, {'form': form})


class MyOrders(TemplateView):
    template_name = 'accounts/my_orders.html'

    def get_context_data(self, **kwargs):
        context = super(MyOrders, self).get_context_data(**kwargs)
        context['orders'] = orders = Order.objects.filter(user=self.request.user).order_by('-pk')
        context['orders_products'] = OrderProduct.objects.filter(order__in=orders)
        return context
