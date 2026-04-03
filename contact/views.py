# contact/views.py

from django.shortcuts import render, redirect
from .models import ContactInfo
from .forms import ContactForm
from django.contrib import messages

def contact_view(request):
    contact_infos = ContactInfo.objects.all()
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Your message has been sent!')
            return redirect('contact')

    return render(request, 'contact/contact_page.html', {
        'contact_infos': contact_infos,
        'form': form
    })
