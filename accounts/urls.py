from django.urls import path
from . import views

urlpatterns = [
    path('register/', views. signup_view, name='register_page'),
    path('login/', views. login_view, name='login_page'),
    path('profile/', views.profile_page, name='profile_page'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/delete/<int:cart_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('logout/', views.logout_page, name='logout_page'),
    path('order/<int:product_id>/', views.place_order, name='place_order'),
    path('payment-method/<int:order_id>/', views.payment_method, name='payment_method'),
    # path('order/success/', views.order_success, name='order_success'),

#Forgotten Password
    path('reset-password/', views.reset_password_request, name='reset_password_request'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('set-new-password/', views.set_new_password, name='set_new_password'),
   
]
