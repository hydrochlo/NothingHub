from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .cart import Cart
from store.models import Product

# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    
    return render(request, "cart/cart.html", {"cart": cart})

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('size')
    color = request.POST.get('color')
    price_increment = request.POST.get('price_increment', 0)
    
    cart.add(
        product=product, 
        quantity=quantity, 
        size=size, 
        color=color, 
        price_increment=price_increment
    )
    
    return redirect('cart_summary')

@require_POST
def cart_update(request, item_key):
    cart = Cart(request)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        # Check if item exists and update
        if item_key in cart.cart:
            cart.cart[item_key]['quantity'] = quantity
            cart.save()
    else:
        cart.remove(item_key)
        
    if request.headers.get('HX-Request'):
        return render(request, "cart/partials/cart_content.html", {"cart": cart})
        
    return redirect('cart_summary')


@require_POST
def cart_remove(request, item_key):
    cart = Cart(request)
    cart.remove(item_key)
    
    if request.headers.get('HX-Request'):
        return render(request, "cart/partials/cart_content.html", {"cart": cart})
        
    return redirect('cart_summary')