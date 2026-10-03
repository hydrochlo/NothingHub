from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ("category_slug",)
    list_display = ("category_name", "category_slug", "created_at")

# Register your models here.
admin.site.register(Category, CategoryAdmin)