from django.contrib import admin
from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ("category_slug",)
    list_display = ("category_name", "category_slug", "created_at")


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"product_slug" : ("product_title",)}
    list_display = ("product_title", "product_slug", "product_stock", "product_is_available")
    
    
# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)