from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    profileImage = models.CharField(max_length=255, default='default.jpg')
    phoneNumber = models.CharField(max_length=15, unique=True, blank=True, null=True)
    address = models.JSONField(blank=True, null=True)  # {'City': ..., 'Country': ..., 'Street': ...}
    role = models.CharField(max_length=10, choices=[('buyer','Buyer'),('seller','Seller')], default='buyer')
    passwordChanagedAt = models.DateTimeField(blank=True, null=True)
    passwordResetCode = models.CharField(max_length=255, blank=True, null=True)
    passwordResetExpiret = models.DateTimeField(blank=True, null=True)
    passwordResetVerifed = models.BooleanField(default=False)
    isVerified = models.BooleanField(default=False)
    IsActive = models.BooleanField(default=True)
    # Wishlists, Cart, Products: ManyToMany to Product (use string ref to avoid circular import)
    Wishlists = models.ManyToManyField('products.Product', related_name='wishlisted_by', blank=True)
    Cart = models.ManyToManyField('products.Product', related_name='in_cart_of', blank=True)
    storeName = models.CharField(max_length=25, unique=True, blank=True, null=True)
    storeDescription = models.CharField(max_length=500, blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    Products = models.ManyToManyField('products.Product', related_name='seller_products', blank=True)
    permissions = models.JSONField(blank=True, null=True, default=list)  # e.g. ["create", "read"]

    def __str__(self):
        return self.username