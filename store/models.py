from django.db import models


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    category_slug = models.SlugField(max_length=100, blank=True, unique=True)
    category_description = models.TextField(max_length=250, blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True, 
        blank=True,
        related_name="children",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category_image = models.ImageField(upload_to='category_images/')
    
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        indexes = [
            models.Index(fields=["id", "category_slug"], name="idx_id_slug_category"),
            models.Index(fields=["created_at"], name="idx_created_at_category"),
        ]
    
    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_title = models.CharField(max_length=200, unique=True)
    product_slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    product_description = models.TextField(blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    product_discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    product_stock = models.IntegerField()
    product_is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=["id", "product_slug"], name="idx_id_slug_product"),
            models.Index(fields=["created_at"], name="idx_created_at_product"),
        ]
    
    def __str__(self):
        return self.product_title

    


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images/")
    
    def __str__(self):
        return f"Image for {self.product.product_title}"
    
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    color = models.CharField(max_length=20)
    size = models.CharField(max_length=3)
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    variant_stocks = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ("product", "color", "size")
    
    def __str__(self):
        return f"{self.product.product_title} - {self.color}/{self.size}"