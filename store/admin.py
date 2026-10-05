from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVariant

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"category_slug" : ("category_name",)}
    list_display = ("category_name", "category_slug", "created_at")


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"product_slug" : ("product_title",)}
    list_display = ("product_title", "product_slug", "product_stock", "product_is_available")
    inlines = [ProductImageInline, ProductVariantInline]