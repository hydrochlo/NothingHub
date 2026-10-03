from django.db import models
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    category_slug = models.SlugField(max_length=100, blank=True, unique=True)
    category_description = models.TextField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category_image = models.ImageField(upload_to='category_images/')
    
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.category_name
    
    def save(self, *args, **kwargs):  # new
        if not self.category_slug:
            self.category_slug = slugify(self.category_name)
        return super().save(*args, **kwargs)

