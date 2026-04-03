from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
#Signup form
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    photo = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'photo', 'password1', 'password2')



#Login form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
