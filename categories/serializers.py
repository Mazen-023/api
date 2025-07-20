from rest_framework import serializers
from .models import Category


# Create your serializers here.

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'imageCategory', 'created_at', 'updated_at'] 