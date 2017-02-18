from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from accounts.models import User


class RegistrationFrom(UserCreationForm):

    rules = forms.BooleanField(required=True, initial=False, widget=forms.CheckboxInput(attrs={'data-toggle':'checkbox'}))
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name',
                  'last_name', 'street', 'postcode', 'city', 'email', 'phone')
    
    def save(self, commit=True): 
        user = super(RegistrationFrom, self).save(commit=False) 
        # wymagana aktywacja konta poprzez link aktywacyjny
        user.is_active = False
        if commit: 
            user.save()
        return user
    
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')

    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError("Ten email został już użyty.")

    #     return email
