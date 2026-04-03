from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.core.paginator import Paginator


# def clothing_products(request):
#     category = get_object_or_404(Category, name='Clothing')
#     products = Product.objects.filter(category=category)
#     return render(request, 'products/clothing_products.html', {'category': category, 'products': products})



def clothing_products(request):
    category = get_object_or_404(Category, name='Clothing')
    products = Product.objects.filter(category=category)

    paginator = Paginator(products, 5)  # 5 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/clothing_products.html', {
        'category': category,
        'page_obj': page_obj
    })
    
def books_products(request):
    category = get_object_or_404(Category, name='Books')
    products = Product.objects.filter(category=category)
    return render(request, 'products/books_products.html', {'category': category, 'products': products})

def shoes_products(request):
    category = get_object_or_404(Category, name='Shoes')
    products = Product.objects.filter(category=category)
    return render(request, 'products/shoes_products.html', {'category': category, 'products': products})


def umbrella_products(request):
    category = get_object_or_404(Category, name='Umbrella')
    products = Product.objects.filter(category=category)
    return render(request, 'products/umbrella_products.html', {'category': category, 'products': products})

def headphone_products(request):
    category = get_object_or_404(Category, name='Headphone')
    products = Product.objects.filter(category=category)
    return render(request, 'products/headphone_products.html', {'category': category, 'products': products})

