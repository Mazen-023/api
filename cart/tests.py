from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User
from products.models import Product
from categories.models import Category
from .models import CartItem

# Create your tests here.

class CartAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='buyer', email='buyer@example.com', password='buyerpass')
        self.category = Category.objects.create(name='Tech', description='Tech category')
        self.product = Product.objects.create(
            name='Phone',
            description='A smart phone',
            price=500.00,
            quantity=5,
            category=self.category,
            seller=self.user
        )

    def test_add_to_cart(self):
        """Check if buyers can add to cart"""
        self.client.login(username='buyer', password='buyerpass')
        url = reverse('cart-add', args=[self.product.id])
        response = self.client.post(url, {'quantity': 2})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(CartItem.objects.filter(user=self.user, product=self.product).exists())

    def test_list_cart(self):
        self.client.login(username='buyer', password='buyerpass')
        CartItem.objects.create(user=self.user, product=self.product, quantity=1)
        url = reverse('cart-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_clear_cart(self):
        self.client.login(username='buyer', password='buyerpass')
        CartItem.objects.create(user=self.user, product=self.product, quantity=1)
        url = reverse('cart-clear')
        response = self.client.put(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CartItem.objects.filter(user=self.user).exists())

    def test_remove_from_cart(self):
        self.client.login(username='buyer', password='buyerpass')
        CartItem.objects.create(user=self.user, product=self.product, quantity=1)
        url = reverse('cart-remove', args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(CartItem.objects.filter(user=self.user, product=self.product).exists())

    def test_permission_required_for_add(self):
        url = reverse('cart-add', args=[self.product.id])
        response = self.client.post(url, {'quantity': 1})
        self.assertEqual(response.status_code, 401)

    def test_permission_required_for_list(self):
        url = reverse('cart-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_permission_required_for_clear(self):
        url = reverse('cart-clear')
        response = self.client.put(url)
        self.assertEqual(response.status_code, 401)

    def test_permission_required_for_remove(self):
        url = reverse('cart-remove', args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)
