from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User
from products.models import Product
from categories.models import Category
from .models import Order, OrderProduct

# Create your tests here.

class OrderAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='buyer', email='buyer@example.com', password='buyerpass')
        self.seller = User.objects.create_user(username='seller', email='seller@example.com', password='sellerpass')
        self.category = Category.objects.create(name='Tech', description='Tech category')
        self.product = Product.objects.create(
            name='Phone',
            description='A smart phone',
            price=500.00,
            quantity=5,
            category=self.category,
            seller=self.seller
        )
        self.order = Order.objects.create(user=self.user, seller=self.seller, totalPrice=500.00, paymentMethod='COD')
        self.order_product = OrderProduct.objects.create(order=self.order, product=self.product, quantity=1)

    def test_create_order(self):
        """Check if buyers can create orders"""
        self.client.login(username='buyer', password='buyerpass')
        url = reverse('order-create')
        data = {
            'products': [{'product_id': self.product.id, 'quantity': 2}],
            'seller': self.seller.id,
            'totalPrice': 1000.00,
            'paymentMethod': 'COD'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Order.objects.filter(user=self.user).count() >= 1)

    def test_list_orders(self):
        """Check if buyers can list orders"""
        self.client.login(username='buyer', password='buyerpass')
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_order(self):
        """Check if buyers can retrieve an order"""
        self.client.login(username='buyer', password='buyerpass')
        url = reverse('order-detail', args=[self.order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.order.id)

    def test_delete_order(self):
        """Check if buyers can delete an order"""
        self.client.login(username='buyer', password='buyerpass')
        url = reverse('order-delete', args=[self.order.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())

    def test_update_order_status(self):
        """Check if buyers can update an order status"""
        self.client.login(username='buyer', password='buyerpass')
        url = reverse('order-update-status', args=[self.order.id, 'Paid'])
        response = self.client.put(url)
        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'Paid')

    def test_get_order_total(self):
        """Check if buyers can get an order total"""
        self.client.login(username='buyer', password='buyerpass')
        url = reverse('order-total')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('total', response.data)

    def test_list_orders_by_user(self):
        """Check if buyers can list orders by user"""
        self.client.login(username='buyer', password='buyerpass')
        url = reverse('order-list-by-user', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_orders_by_product(self):
        """Check if buyers can list orders by product"""
        self.client.login(username='buyer', password='buyerpass')
        url = reverse('order-list-by-product', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('count', response.data)

    def test_list_orders_by_status(self):
        """Check if buyers can list orders by status"""
        self.client.login(username='buyer', password='buyerpass')
        url = reverse('order-list-by-status', args=['Pending'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_user_orders_by_status(self):
        """Check if buyers can list user orders by status"""
        self.client.login(username='buyer', password='buyerpass')
        url = reverse('order-list-user-status', args=[self.user.id, 'Pending'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_permission_required_for_create(self):
        """Check if users can create orders"""
        url = reverse('order-create')
        data = {
            'products': [{'product_id': self.product.id, 'quantity': 2}],
            'seller': self.seller.id,
            'totalPrice': 1000.00,
            'paymentMethod': 'COD'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_permission_required_for_delete(self):
        """Check if users can delete orders"""
        url = reverse('order-delete', args=[self.order.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)
