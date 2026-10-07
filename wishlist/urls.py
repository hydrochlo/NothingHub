from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path("", views.wishlist_dashboard, name="wishlist_dashboard"),
    path("toggle/<int:product_id>/", views.wishlist_toggle, name="wishlist_toggle"),
    path("move-to-cart/<int:product_id>/", views.move_to_cart, name="move_to_cart"),
]