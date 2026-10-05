from django.urls import path, include
from .views import ProductListView, ProductDetailView

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product_list"),
    path("<slug:category_slug>/<slug:product_slug>/", ProductDetailView.as_view(), name="product_detail"),
]