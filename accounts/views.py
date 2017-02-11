from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic.edit import UpdateView, View

from accounts.forms import UserRegistration
from accounts.models import User

class UserUpdate(UpdateView):
    model = User
    fields = ['first_name','last_name', 'street', 'postcode', 'city', 'email' ,'phone']
    template_name_suffix = '_update_form'


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

class Registration(View):
    template_name = 'registration/registration.html'

    def get(self, request, *args, **kwargs):
        form = UserRegistration()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserRegistration(request.POST)

        if form.is_valid():
            user = form.save()
            html_message = render_to_string(
                'accounts/activation_email.html', {'activation_key': user.activation_key})
            user.email_user('Aktywacja konta', '', html_message=html_message)
            messages.success(
                request, 'Rejestracja przebiegła pomyślnie! Odbierz teraz waidomość wysłaną na podany adres email, aby aktywować swoje konto!')
            return HttpResponseRedirect('/accounts/login')

        return render(request, self.template_name, {'form': form})
