from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

from store.models import Product
from cart.cart import Cart
from .models import Wishlist

@login_required
@require_POST
def wishlist_toggle(request, product_id):
    """Toggle a product in/out of the user's wishlist (supports AJAX and standard POST forms)."""
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if not created:
        wishlist_item.delete()
        is_wishlisted = False
        message = f"Removed '{product.product_title}' from your wishlist."
    else:
        is_wishlisted = True
        message = f"Added '{product.product_title}' to your wishlist."

    is_ajax = (
        request.headers.get("x-requested-with") == "XMLHttpRequest" 
        or request.headers.get("HX-Request")
    )

    if is_ajax:
        return JsonResponse({
            "status": "success",
            "is_wishlisted": is_wishlisted,
            "message": message,
            "total_count": request.user.wishlist_items.count(),
        })

    messages.info(request, message)
    return redirect("wishlist:wishlist_dashboard")

@login_required
def wishlist_dashboard(request):
    """Render the Wishlist management dashboard."""
    wishlist_items = request.user.wishlist_items.select_related("product").all()
    return render(request, "wishlist/dashboard.html", {"wishlist_items": wishlist_items})

@login_required
@require_POST
def move_to_cart(request, product_id):
    """Transfer an item from Wishlist to the session Cart and remove from Wishlist."""
    product = get_object_or_404(Product, id=product_id)

    # 1. Add product to session cart
    cart = Cart(request)
    cart.add(
        product=product,
        quantity=int(request.POST.get("quantity", 1)),
        size=request.POST.get("size"),
        color=request.POST.get("color"),
    )

    # 2. Delete item from user's wishlist
    Wishlist.objects.filter(user=request.user, product=product).delete()
    messages.success(request, f"Moved '{product.product_title}' to your cart.")

    return redirect("wishlist:wishlist_dashboard")