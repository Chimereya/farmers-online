from django.urls import path
from . import views



urlpatterns = [
    path('', views.home_view, name='home'),
    path('<category_slug>/', views.product_category, name='category'),
    path('<int:id>/<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),
    path('products/cart/', views.view_cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('get-total-cost/', views.get_total_cost, name='get_total_cost'),
    path('products/checkout/', views.checkout_view, name='checkout'),
    path('products/payment/', views.payment_view, name='payment_url'),
    
]

