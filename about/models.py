from django.db import models

# Create your models here.
# yourapp/models.py


class About(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    bio = models.TextField()
    photo = models.ImageField(upload_to='about_photos/')

    def __str__(self):
        return self.name
