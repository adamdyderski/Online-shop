from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from .forms import AddToCartForm, OrderbyForm
from .models import Product,Category


class List(ListView):
    model = Product
    context_object_name = "products"
    template_name = "shop_app/products_list.html"

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        context['random_products'] = Product.objects.filter(quantity__gt=0).order_by('?')[:3]
        context['orderby_form'] = OrderbyForm(initial=self.request.GET)
        context['title'] = self.get_title()
        return context
    
    def get_title(self):
        if self.kwargs.get('category_pk'):
            title = Category.objects.get(id=self.kwargs['category_pk'])
            return 'Kategoria: {}'.format(title.name)
        else:
            return 'Wszytskie'

    def get_queryset(self):
        order = self.request.GET.get('orderby', 'name')
        qs = self.model.objects.filter(quantity__gt=0).order_by(order)
        # filtr kategoria
        if self.kwargs.get('category_pk'):
            qs = qs.filter(category=self.kwargs['category_pk'])

        return qs

class Details(DetailView, FormMixin):
    model = Product
    template_name = "shop_app/product_details.html"
    form_class = AddToCartForm

    def availability(self):
        q = self.object.quantity
        return 'brak' if q == 0 else 'na wyczerpaniu' if q < 5 else 'dostępny'  

    def get_context_data(self, **kwargs):
        context = super(Details, self).get_context_data(**kwargs)
        context['availability'] = self.availability()
        return context
    
    