from rest_framework import serializers
from .models import CartItem
from products.serializers import ProductSerializer

# Create your serializers here.

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=ProductSerializer.Meta.model.objects.all(), source='product', write_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'user', 'product', 'product_id', 'quantity', 'added_at', 'updated_at'] 