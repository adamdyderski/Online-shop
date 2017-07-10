from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from .forms import AddToCartForm, OrderbyForm
from .models import Category, Product


class List(ListView):
    model = Product
    context_object_name = "products"
    template_name = "shop_app/products_list.html"

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        context['random_products'] = self.get_random_products(3)
        context['orderby_form'] = OrderbyForm(initial=self.request.GET)
        context['title'] = self.get_title()
        return context

    def get_random_products(self, n):
        return self.model.objects.filter(quantity__gt=0).order_by('?')[:n]

    def get_title(self, title="Wszystkie"):
        if self.kwargs.get('category_pk'):
            c = Category.objects.get(id=self.kwargs['category_pk'])
            title = 'Kategoria: {}'.format(c)
        return title

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
