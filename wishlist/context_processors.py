def wishlist(request):
    if request.user.is_authenticated:
        user_wishlist_ids = list(request.user.wishlist_items.values_list('product_id', flat=True))
    else:
        user_wishlist_ids = []
        
    return {
        'user_wishlist_ids': user_wishlist_ids
    }