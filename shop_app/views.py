from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from .forms import AddToCartForm
from .models import Product


class Home(ListView):
    model = Product
    context_object_name = "products"
    template_name = "shop_app/home.html"


class ProductDetails(DetailView, FormMixin):
    model = Product
    template_name = "shop_app/product_details.html"
    form_class = AddToCartForm

    def availability(self):
        q = self.object.quantity
        return 'brak' if q == 0 else 'na wyczerpaniu' if q < 5 else 'dostępny'  

    def get_context_data(self, **kwargs):
        context = super(ProductDetails, self).get_context_data(**kwargs)
        context['availability'] = self.availability()
        return context
    
    