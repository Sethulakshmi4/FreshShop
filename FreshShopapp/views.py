from .models import Product
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.db.models import Q


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect('view_products')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

@never_cache
@login_required
def view_products(request):
    products = Product.objects.all()
    # query = request.GET.get('q',' ')
    # # Fetch all products from the database
    
    # if query:
    #     products = products.filter(
    #         Q(name_icontains=query) | Q(description_icontains=query)
    #     )
    
    # Set up pagination
    paginator = Paginator(products, 3)  # 3 products per page
    page_number = request.GET.get('page')  # Get the page number from the URL
    page_obj = paginator.get_page(page_number)  # Get the current page of products
    
    # Pass the page_obj to the template to display the paginated products
    return render(request, 'view_products.html', {'page_obj': page_obj})

@never_cache
@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')

@never_cache
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'view_cart.html', {'cart_items': cart_items})

@never_cache
@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate subtotals and total price
    for item in cart_items:
        item.subtotal = item.product.price * item.quantity  # Add subtotal to each cart item

    total_price = sum(item.subtotal for item in cart_items)

    if request.method == "POST":
         # Mark the cart as completed (i.e., this is the order)
        cart.completed = True
        cart.save()
        # Optionally, you can send a confirmation email or display a success message
        messages.success(request, f"Your order has been placed!")
        return redirect('view_orders')

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})

@never_cache
@login_required
def view_orders(request):
    # Fetch completed carts (orders) for the user
    completed_carts = Cart.objects.filter(user=request.user, completed=True).order_by('-id')

    # Retrieve cart items for each completed cart
    order_details = []
    for cart in completed_carts:
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        order_details.append({'cart': cart, 'cart_items': cart_items, 'total_price': total_price})

    return render(request, 'view_orders.html', {'order_details': order_details})
