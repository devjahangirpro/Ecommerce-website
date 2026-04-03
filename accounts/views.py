from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from .models import Cart, Order,User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.conf import settings
#forgotten password
from django.core.mail import send_mail
import random
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login_page')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register_form.html', {'form': form})


#Login form

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('home_page')  
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login_form.html', {'form': form})


#profile page
@login_required
def profile_page(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    orders = Order.objects.filter(user=user).order_by('-ordered_at')  # ✅ fixed here
    total_cart_value = sum(item.total_price for item in cart_items)

    context = {
        'user': user,
        'cart_items': cart_items,
        'orders': orders,
        'total_cart_value': total_cart_value,
    }
    return render(request, 'accounts/profile_page.html', context)




@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Get quantity from form, default to 1 if missing or invalid
        quantity = request.POST.get('quantity')
        try:
            quantity = int(quantity)
            if quantity < 1:
                quantity = 1
        except (ValueError, TypeError):
            quantity = 1
    else:
        quantity = 1

    # Check if cart item already exists for this user and product
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        # If exists, add the new quantity to existing
        cart_item.quantity += quantity
        cart_item.save()

    return redirect('profile_page') 
#delete cart
@login_required
def delete_cart_item(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)

    if request.method == "POST":
        cart_item.delete()
    
    return redirect('profile_page') 


#logout page
def logout_page(request):
    logout(request)
    return redirect('home_page')



@login_required
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if full_name and phone and address:
            order = Order.objects.create(   # <-- ekhane order instance assign kora holo
                user=request.user,
                product=product,
                full_name=full_name,
                phone=phone,
                address=address
            )
            return redirect('payment_method', order_id=order.id)

        else:
            error = "All fields are required."
            return render(request, 'accounts/order_form.html', {'product': product, 'error': error})

    return render(request, 'accounts/order_form.html', {'product': product})




#payment method
def payment_method(request, order_id):
    order = Order.objects.get(id=order_id)

    if request.method == 'POST':
        payment_option = request.POST['payment_method']
        order.payment_method = payment_option
        order.status = 'confirmed'  # or keep 'pending' until admin approves payment
        order.save()

        return redirect('home_page')  # redirect to a success page

    return render(request, 'accounts/payment_method.html', {'order': order})





# Forgot Password Request View
def reset_password_request(request):
    if request.method == 'POST':
        method = request.POST.get('method')
        username = request.POST.get('username')
        input_value = request.POST.get('input_value')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Username does not exist.")
            return redirect('reset_password_request')

        otp = str(random.randint(100000, 999999))

        if method == 'email':
            if user.email != input_value:
                messages.error(request, "Email does not match with username.")
                return redirect('reset_password_request')
            # Send email OTP
            send_mail(
                "Your OTP for Password Reset",
                f"Hello {user.username}, your OTP is {otp}",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
        elif method == 'phone':
            # Integrate Twilio or any SMS API here in future
            print(f"Send OTP {otp} to phone {input_value}")  # Placeholder for now
        else:
            messages.error(request, "Invalid method selected.")
            return redirect('reset_password_request')

        # Store OTP and user in session
        request.session['reset_user_id'] = user.id
        request.session['reset_otp'] = otp
        request.session['reset_method'] = method

        return redirect('verify_otp')

    return render(request, 'accounts/reset_password.html')



# Verify OTP View
def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('reset_otp')

        if entered_otp == session_otp:
            # OTP correct, go to set new password
            return redirect('set_new_password')
        else:
            messages.error(request, "Invalid OTP.")
            return redirect('verify_otp')

    return render(request, 'accounts/verify_otp.html')


# Set New Password View
def set_new_password(request):
    user_id = request.session.get('reset_user_id')

    if not user_id:
        messages.error(request, "Session expired. Please try again.")
        return redirect('reset_password_request')

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('set_new_password')

        try:
            user = User.objects.get(id=user_id)
            user.set_password(password)
            user.save()

            # clear session
            request.session.flush()

            messages.success(request, "Password reset successful. Please login.")
            return redirect('login_page')
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('reset_password_request')

    return render(request, 'accounts/set_new_password.html')

