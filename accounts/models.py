from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from core.models import TimeStampedModel, UUIDModel

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError("Email address is mandetory!")
        
        if not username:
            raise ValueError("User must have an username!")
    
        user = self.model(
            email = self.normalize_email(email),
            username=username,
            first_name=first_name, 
            last_name=last_name
        )
        
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self.db)
        
        return user
    
class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    # phone_number = models.CharField(max_length=50)
    
    # required
    joining_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    
    # tell django to user email instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    
    # This connects CustomManager to User model
    objects = UserManager()
    
    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, add_label):
        return True
    
    
    
class UserProfile(models.Model):
    # Link to your custom User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True)
    
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    avatar_url = models.URLField(max_length=500, blank=True, null=True)  # To store Google OAuth photo link
    
    # Shipping Address
    shipping_address_line1 = models.CharField(max_length=255, blank=True)
    shipping_address_line2 = models.CharField(max_length=255, blank=True)
    shipping_city = models.CharField(max_length=100, blank=True)
    shipping_postal_code = models.CharField(max_length=20, blank=True)
    shipping_country = models.CharField(max_length=100, blank=True)
    
    # Billing Address
    billing_address_line1 = models.CharField(max_length=255, blank=True)
    billing_address_line2 = models.CharField(max_length=255, blank=True)
    billing_city = models.CharField(max_length=100, blank=True)
    billing_postal_code = models.CharField(max_length=20, blank=True)
    billing_country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Profile of {self.user.email}"
    
    @property
    def get_avatar_url(self):
        """Helper to return local uploaded avatar, Google picture, or default placeholder."""
        if self.avatar:
            return self.avatar.url
        if self.avatar_url:
            return self.avatar_url
        return '/static/images/avatar.jpg'
