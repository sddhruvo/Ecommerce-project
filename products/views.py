from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Product, Review

class ProductList(ListView):
    model = Product
    ordering = '-created_at'

class ProductDetail(DetailView):
    model = Product
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['object'] = self.object
        context ['reviews'] = self.object.review_set.all()
        return context