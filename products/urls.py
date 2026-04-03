from django.urls import path
from . import views

urlpatterns = [
    path('clothing/', views.clothing_products, name='clothing_products'),
    path('books/', views.books_products, name='books_products'),
    path('shoes/', views.shoes_products, name='shoes_products'),
    path('umbrella/', views.umbrella_products, name='umbrella_products'),
    path('headphone/', views.headphone_products, name='headphone_products'),
    
    
]
