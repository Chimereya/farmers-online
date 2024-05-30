from django.urls import path
from . import views



urlpatterns = [
    path('', views.home_view, name='home'),
    path('<category_slug>/', views.category_view, name='category'),

]

