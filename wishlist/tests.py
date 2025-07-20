from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User
from products.models import Product
from categories.models import Category
from .models import WishlistItem

# Create your tests here.

class WishlistAPITestCase(APITestCase):
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

    def test_add_to_wishlist(self):
        self.client.login(username='buyer', password='buyerpass')
        url = reverse('wishlist-add', args=[self.product.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(WishlistItem.objects.filter(user=self.user, product=self.product).exists())

    def test_remove_from_wishlist(self):
        self.client.login(username='buyer', password='buyerpass')
        WishlistItem.objects.create(user=self.user, product=self.product)
        url = reverse('wishlist-remove', args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(WishlistItem.objects.filter(user=self.user, product=self.product).exists())

    def test_list_wishlist(self):
        self.client.login(username='buyer', password='buyerpass')
        WishlistItem.objects.create(user=self.user, product=self.product)
        url = reverse('wishlist-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_permission_required_for_add(self):
        url = reverse('wishlist-add', args=[self.product.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 401)

    def test_permission_required_for_remove(self):
        url = reverse('wishlist-remove', args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    def test_permission_required_for_list(self):
        url = reverse('wishlist-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
