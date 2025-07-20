from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User
from .models import Category
from products.models import Product

# Create your tests here.

class CategoryAPITestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', email='admin@example.com', password='adminpass', role='admin', is_staff=True)
        self.user = User.objects.create_user(username='user', email='user@example.com', password='userpass')
        self.category = Category.objects.create(name='Books', description='Books category')
        self.product = Product.objects.create(
            name='Novel',
            description='A great novel',
            price=20.00,
            quantity=5,
            category=self.category,
            seller=self.user
        )

    def test_create_category(self):
        """Check if admins can create categories"""
        self.client.login(username='admin', password='adminpass')
        url = reverse('category-create')
        data = {'name': 'Music', 'description': 'Music category'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Category.objects.filter(name='Music').exists())

    def test_list_categories(self):
        """Check if users can list categories"""
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_category(self):
        """Check if users can retrieve a category"""
        url = reverse('category-detail', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Books')

    def test_update_category(self):
        """Check if admins can update categories"""
        self.client.login(username='admin', password='adminpass')
        url = reverse('category-update', args=[self.category.id])
        response = self.client.put(url, {'name': 'Updated Books', 'description': 'Updated description'})
        self.assertEqual(response.status_code, 200)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Books')

    def test_update_category_image(self):
        """Check if admins can update category image"""
        self.client.login(username='admin', password='adminpass')
        url = reverse('category-update-image', args=[self.category.id])
        response = self.client.put(url, {'imageCategory': 'newimage.jpg'})
        self.assertEqual(response.status_code, 200)
        self.category.refresh_from_db()
        self.assertEqual(self.category.imageCategory, 'newimage.jpg')

    def test_delete_category(self):
        """Check if admins can delete categories"""
        self.client.login(username='admin', password='adminpass')
        url = reverse('category-delete', args=[self.category.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())

    def test_list_category_products(self):
        """Check if users can list category products"""
        url = reverse('category-products', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_permission_required_for_create(self):
        """Check if users can create categories"""
        self.client.login(username='user', password='userpass')
        url = reverse('category-create')
        data = {'name': 'Unauthorized', 'description': 'Should fail'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

    def test_permission_required_for_update(self):
        """Check if users can update categories"""
        self.client.login(username='user', password='userpass')
        url = reverse('category-update', args=[self.category.id])
        response = self.client.put(url, {'name': 'No Auth', 'description': 'No Auth'})
        self.assertEqual(response.status_code, 403)

    def test_permission_required_for_delete(self):
        """Check if users can delete categories"""
        self.client.login(username='user', password='userpass')
        url = reverse('category-delete', args=[self.category.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
