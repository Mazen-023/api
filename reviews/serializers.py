from rest_framework import serializers
from .models import Review
from products.serializers import ProductSerializer

# Create your serializers here.

class ReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=ProductSerializer.Meta.model.objects.all(), source='product', write_only=True)
    user = serializers.StringRelatedField(read_only=True)
    user_name = serializers.SerializerMethodField()

    def get_user_name(self, obj):
        user = obj.user
        if hasattr(user, 'get_full_name') and user.get_full_name():
            return user.get_full_name()
        return user.username if hasattr(user, 'username') else str(user)

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_name', 'product', 'product_id', 'rating', 'review', 'created_at', 'updated_at']