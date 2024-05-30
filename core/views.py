from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  TemplateView)
from django.urls import reverse_lazy
from .models import (ProductCategory,
                     Product )
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string, get_template



def home_view(request):
    products = Product.objects.filter(status=1)
    categories = ProductCategory.objects.all()
    
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'core/home.html', context)


def product_category(request, category_slug=None):
    product_category = None
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    # if category slug exists, get the slug
    if category_slug:
        product_category = get_object_or_404(ProductCategory, slug=category_slug)
        # filter and display the products by the category
        products = products.filter(product_category=product_category)
    
    context = {
        'category': product_category,
        'categories': categories,
        'products': products
    }
    return render(request, 'core/category.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name='core/detail.html'
        
