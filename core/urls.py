from django.urls import path
from . import views



urlpatterns = [
    path('', views.home_view, name='home'),
    path('<category_slug>/', views.product_category, name='category'),
    path('<int:id>/<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),


]

