from django.shortcuts import render
from accounts.forms import UserRegistration
from django.views.generic.edit import CreateView,View
from django.template.loader import render_to_string
from django.contrib import messages 
from django.http import HttpResponse, HttpResponseRedirect

# class RegistrationView(CreateView):
#     template_name = 'accounts/registration.html'
#     form_class = UserRegistration
#     success_url = '/accounts/registration/'

class Registration(View): 
    template_name = 'accounts/registration.html'
    form_class = UserRegistration
    success_url = '/accounts/registration/'
 
    def get(self, request, *args, **kwargs):      
        form = UserRegistration() 
        return render(request, self.template_name , {'form': form}) 
 
    def post(self, request, *args, **kwargs):     
        form = UserRegistration(request.POST) 
        
        if form.is_valid():  
            user = form.save() 
            html_message = render_to_string('accounts/activation_email.html', {'activation_key': user.activation_key}) 
            user.send_mail('Aktywacja konta','', html_message=html_message) 
            messages.success(request, 'Rejestracja przebiegła pomyślnie! Odbierz teraz waidomość wysłaną na podany adres email, aby aktywować swoje konto!') 
            return HttpResponseRedirect('/accounts/login')           
         
        return render(request, self.template_name , {'form': form}) 


