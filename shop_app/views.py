from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from .forms import AddToCartForm, OrderbyForm
from .models import Product


class Home(ListView):
    context_object_name = "products"
    template_name = "shop_app/products_list.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['random'] = Product.objects.order_by('?')[:3]
        context['orderby'] = OrderbyForm(initial=self.request.GET)
        return context

    def get_queryset(self):
        order = self.request.GET.get('orderby', 'name')
        return Product.objects.filter(quantity__gt=0).order_by(order)


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
    
    