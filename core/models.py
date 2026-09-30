import uuid
from django.db import models

# 1. Base Timestamp Model (Used by almost ALL models)
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) # Set once on creation
    updated_at = models.DateTimeField(auto_now=True)     # Automatically updates on save

    class Meta:
        abstract = True  # Ensures no database table is created for this model directly

# 2. Base UUID Model (Optional: if you prefer UUIDs over integer IDs for security)
class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

# 3. Soft Delete Base Model (Optional: to hide items without actually deleting from DB)
class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

# 4. Global Store Settings (Concrete Model - creates actual table)
class StoreSetting(TimeStampedModel):
    site_name = models.CharField(max_length=100, default="NothigHub")
    support_email = models.EmailField(default="sadat2151@gmail.com")
    # tax_rate_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    # maintenance_mode = models.BooleanField(default=False)

    def __str__(self):
        return self.site_name