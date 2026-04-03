from django.shortcuts import render

# Create your views here.
# yourapp/views.py

from django.shortcuts import render
from .models import About

def about_view(request):
    about = About.objects.first()  
    return render(request, 'about/about_page.html', {'about': about})
