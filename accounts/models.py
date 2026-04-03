from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from products.models import Product 
from django.conf import settings  # ✅ use settings for AUTH_USER_MODEL

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)

    photo = models.ImageField(upload_to='profile_photos/', default='default.jpg')

    def __str__(self):
        return self.username

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

    @property
    def total_price(self):
        return self.product.price * self.quantity
    
    
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"





class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, default="No Name")
    phone = models.CharField(max_length=20, default="0000000000")
    address = models.CharField(max_length=255, default="No Address")
    ordered_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, default='Pending')

    class Meta:
        ordering = ['-ordered_at']  # show latest orders first

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    
   #forgotten password 



class PasswordResetOTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10)  # 'email' or 'phone'

    def __str__(self):
        return f"{self.user.username} - {self.method}"