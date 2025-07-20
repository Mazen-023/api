from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'profileImage', 'phoneNumber', 'first_name', 'last_name', 'address', 'role',
            'isVerified', 'IsActive', 'storeName', 'storeDescription', 'rating', 'permissions',
        ]
        read_only_fields = ['id', 'isVerified', 'IsActive', 'rating']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirmation = serializers.CharField(write_only=True, required=False)  # Now optional
    role = serializers.ChoiceField(choices=[('buyer', 'Buyer'), ('seller', 'Seller')], required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirmation', 'first_name', 'last_name', 'role']
        read_only_fields = ['id']

    def validate(self, data):
        # Only check if confirmation is provided
        confirmation = data.get('confirmation', None)
        if confirmation is not None and data['password'] != confirmation:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirmation', None)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user