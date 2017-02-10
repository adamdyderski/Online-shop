from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from accounts.models import User


class UserRegistration(UserCreationForm):

    # walidacja
    postcode_validator = RegexValidator("^\d{2}\-?\d{3}$", "Podaj poprawny kod pocztowy")
    phone_validator = RegexValidator("^[0-9-+ ]{9,20}$", "Podaj poprawny numer telefonu")
    postcode = forms.CharField(label="Kod pocztowy",max_length=6, required=True, help_text='np.12-345',validators=[postcode_validator])
    phone = forms.CharField(label="Telefon", max_length=20, required=True, validators=[phone_validator])

    rules = forms.BooleanField(required=True, initial=False, widget=forms.CheckboxInput(attrs={'class':'custom-checkbox', 'data-toogle':'checkbox'}))
    

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name',
                  'last_name', 'street', 'postcode', 'city', 'email', 'phone')

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')

    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError("Ten email został już użyty.")

    #     return email
