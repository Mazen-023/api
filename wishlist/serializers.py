from rest_framework import serializers
from .models import WishlistItem
from products.serializers import ProductSerializer

# Create your serializers here.

class WishlistItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=ProductSerializer.Meta.model.objects.all(), source='product', write_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = WishlistItem
        fields = ['id', 'user', 'product', 'product_id', 'added_at'] 