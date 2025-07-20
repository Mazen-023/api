from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderProduct
from .serializers import OrderSerializer, OrderProductSerializer
from products.models import Product
from accounts.models import User
from django.db.models import Sum

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    # Expecting products as a list of {product_id, quantity}
    products_data = request.data.get('products')
    seller_id = request.data.get('seller')
    total_price = request.data.get('totalPrice')
    payment_method = request.data.get('paymentMethod', 'COD')

    # Validate required fields
    if products_data is None or not isinstance(products_data, list) or len(products_data) == 0:
        return Response({'detail': 'Products list is required and cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)
    if not seller_id:
        return Response({'detail': 'Seller is required.'}, status=status.HTTP_400_BAD_REQUEST)
    if not total_price:
        return Response({'detail': 'Total price is required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Validate seller
    try:
        seller = User.objects.get(pk=seller_id)
    except User.DoesNotExist:
        return Response({'detail': 'Seller not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Validate each product
    valid_products = []
    for item in products_data:
        product_id = item.get('product_id')
        quantity = item.get('quantity')
        if not product_id or not quantity or int(quantity) <= 0:
            continue
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            continue
        valid_products.append((product, int(quantity)))

    if not valid_products:
        return Response({'detail': 'No valid products to order.'}, status=status.HTTP_400_BAD_REQUEST)

    order = Order.objects.create(user=request.user, seller=seller, totalPrice=total_price, paymentMethod=payment_method)
    for product, quantity in valid_products:
        OrderProduct.objects.create(order=order, product=product, quantity=quantity)
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_orders(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_order(request, pk):
    try:
        order = Order.objects.get(pk=pk, user=request.user)
    except Order.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = OrderSerializer(order)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request, pk):
    try:
        order = Order.objects.get(pk=pk, user=request.user)
    except Order.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    order.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_order_status(request, pk, status_str):
    try:
        order = Order.objects.get(pk=pk, user=request.user)
    except Order.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    if status_str not in dict(Order.STATUS_CHOICES):
        return Response({'detail': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)
    order.status = status_str
    order.save()
    serializer = OrderSerializer(order)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_total(request):
    total = Order.objects.filter(user=request.user).aggregate(Sum('totalPrice'))['totalPrice__sum'] or 0
    return Response({'total': total})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_orders_by_user(request, user_id):
    orders = Order.objects.filter(user_id=user_id)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_orders_by_product(request, product_id):
    count = OrderProduct.objects.filter(product_id=product_id).count()
    return Response({'count': count})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_orders_by_status(request, status_str):
    orders = Order.objects.filter(status=status_str)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_orders_by_status(request, user_id, status_str):
    orders = Order.objects.filter(user_id=user_id, status=status_str)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
