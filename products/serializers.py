from rest_framework import serializers
from .models import Product
from categories.models import Category
from categories.serializers import CategorySerializer

# Create your serializers here.

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    seller = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity', 'category', 'category_id', 'imageProduct', 'seller', 'created_at', 'updated_at']
