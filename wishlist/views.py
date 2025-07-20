from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import WishlistItem
from .serializers import WishlistItemSerializer
from products.models import Product

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
    # Prevent duplicate wishlist items
    if WishlistItem.objects.filter(user=request.user, product=product).exists():
        return Response({'detail': 'Product already in wishlist.'}, status=status.HTTP_400_BAD_REQUEST)
    wishlist_item = WishlistItem.objects.create(user=request.user, product=product)
    serializer = WishlistItemSerializer(wishlist_item)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request, product_id):
    try:
        wishlist_item = WishlistItem.objects.get(user=request.user, product_id=product_id)
    except WishlistItem.DoesNotExist:
        return Response({'detail': 'Product not in wishlist.'}, status=status.HTTP_404_NOT_FOUND)
    wishlist_item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_wishlist(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    serializer = WishlistItemSerializer(wishlist_items, many=True)
    return Response(serializer.data)
