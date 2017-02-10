from django import forms
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistration(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name',
                  'last_name', 'street', 'postcode', 'city', 'email', 'phone')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ten email został już użyty.")

        return email
