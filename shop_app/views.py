from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from .models import Product


class Home(ListView):
    model = Product
    context_object_name = "products"
    template_name = "shop_app/home.html"
