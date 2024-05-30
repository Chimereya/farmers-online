from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import (ProductCategory,
                     Product )
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage,\
PageNotAnInteger
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


def category_view(request, category_slug=None):
    category = None
    products = Product.objects.all()
    # if category slug exists, get the slug
    if category_slug:
        category = get_object_or_404(Product, slug=category_slug)
        # filter and display the products by the category
        products = products.filter(category=category)
    else:
        messages.error()
        return redirect('home')
    context = {
        'category': category,
        'categories': categories
    }
    return render(request, 'core/category.html', context)
        
