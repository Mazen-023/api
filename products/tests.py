from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User
from categories.models import Category
from .models import Product

# Create your tests here.

class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='seller', email='seller@example.com', password='sellerpass')
        self.category = Category.objects.create(name='Electronics', description='Electronics category')
        self.product = Product.objects.create(
            name='Laptop',
            description='A powerful laptop',
            price=1000.00,
            quantity=10,
            category=self.category,
            seller=self.user
        )

    def test_create_product(self):
        """Check if sellers can create products"""
        self.client.login(username='seller', password='sellerpass')
        url = reverse('product-create')
        data = {
            'name': 'Phone',
            'description': 'A smart phone',
            'price': 500.00,
            'quantity': 5,
            'category_id': self.category.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Product.objects.filter(name='Phone').exists())

    def test_list_products(self):
        """Check if users can list products"""
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_product(self):
        """Check if users can retrieve a product"""
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Laptop')

    def test_update_product(self):
        """Check if sellers can update their products"""
        self.client.login(username='seller', password='sellerpass')
        url = reverse('product-update', args=[self.product.id])
        response = self.client.put(url, {
            'name': 'Updated Laptop',
            'description': 'Updated description',
            'price': 1200.00,
            'quantity': 8,
            'category_id': self.category.id
        })
        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Laptop')

    def test_delete_product(self):
        """Check if sellers can delete their products"""
        self.client.login(username='seller', password='sellerpass')
        url = reverse('product-delete', args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_update_product_image(self):
        self.client.login(username='seller', password='sellerpass')
        url = reverse('product-update-image', args=[self.product.id])
        response = self.client.put(url, {'imageProduct': 'newimage.jpg'})
        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.imageProduct, 'newimage.jpg')

    def test_permission_required_for_create(self):
        """Check if users can create products"""
        url = reverse('product-create')
        data = {
            'name': 'Tablet',
            'description': 'A tablet',
            'price': 300.00,
            'quantity': 3,
            'category_id': self.category.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)

    def test_permission_required_for_update(self):
        """Check if users can update products"""
        url = reverse('product-update', args=[self.product.id])
        response = self.client.put(url, {
            'name': 'No Auth',
            'description': 'No Auth',
            'price': 100.00,
            'quantity': 1,
            'category_id': self.category.id
        })
        self.assertEqual(response.status_code, 401)

    def test_permission_required_for_delete(self):
        """Check if users can delete products"""
        url = reverse('product-delete', args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)
