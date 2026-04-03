from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Order


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'phone', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('phone', 'photo')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'full_name', 'phone', 'address', 'ordered_at', 'status')
    list_filter = ('status', 'ordered_at')
    search_fields = ('user__username', 'product__name', 'full_name', 'phone', 'address')
    ordering = ('-ordered_at',)