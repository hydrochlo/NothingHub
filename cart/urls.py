from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    path("", views.cart_summary, name="cart_summary"),
    path("add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("update/<str:item_key>/", views.cart_update, name="cart_update"), # Changed to <str:item_key>
    path("remove/<str:item_key>/", views.cart_remove, name="cart_remove"),
]