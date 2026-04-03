# contact/admin.py

from django.contrib import admin
from .models import ContactInfo, ContactMessage

admin.site.register(ContactInfo)
admin.site.register(ContactMessage)
