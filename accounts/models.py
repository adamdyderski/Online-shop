import hashlib
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


def get_activation_key():
    return hashlib.sha1((uuid.uuid1().hex).encode('utf-8')).hexdigest()


class User(AbstractUser):
    #  pola wymagane
    email = models.EmailField(_('email address'), max_length=50)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    
    is_active = models.BooleanField(_('active'), default=False)

    #   dodatkowe dane
    street = models.CharField(max_length=100, verbose_name="Ulica i nr domu")
    postcode = models.CharField(max_length=6, verbose_name="Kod pocztowy")
    city = models.CharField(max_length=50, verbose_name="Miasto")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    activation_key = models.CharField(
        max_length=40, verbose_name="Kod aktywacyjny (SHA1)", default=get_activation_key)
