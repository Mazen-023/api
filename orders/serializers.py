from rest_framework import serializers
from .models import Order, OrderProduct
from products.serializers import ProductSerializer

# Create your serializers here.

class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=ProductSerializer.Meta.model.objects.all(), source='product', write_only=True)

    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'product_id', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    seller = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'seller', 'totalPrice', 'paymentMethod', 'status', 'order_products', 'created_at', 'updated_at'] 