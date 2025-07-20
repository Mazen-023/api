from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User
from products.models import Product
from categories.models import Category
from .models import Review

# Create your tests here.

class ReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='buyer', email='buyer@example.com', password='buyerpass')
        self.other_user = User.objects.create_user(username='other_buyer', email='other@example.com', password='otherpass')
        self.category = Category.objects.create(name='Tech', description='Tech category')
        self.product = Product.objects.create(
            name='Phone',
            description='A smart phone',
            price=500.00,
            quantity=5,
            category=self.category,
            seller=self.user
        )
        # Create a review for the other user (for listing)
        self.other_review = Review.objects.create(user=self.other_user, product=self.product, rating=5, review='Great!')
        # Create a review for the main user (for update/delete tests)
        self.review = Review.objects.create(user=self.user, product=self.product, rating=4, review='Good!')

    def test_add_review(self):
        # Create a new user for this test since both users already have reviews
        new_user = User.objects.create_user(username='new_buyer', email='new@example.com', password='newpass')
        self.client.login(username='new_buyer', password='newpass')
        url = reverse('review-add', args=[self.product.id])
        data = {'rating': 3, 'review': 'Okay phone'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Review.objects.filter(user=new_user, product=self.product, rating=3).exists())

    def test_list_reviews(self):
        url = reverse('review-list', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_review(self):
        self.client.login(username='buyer', password='buyerpass')
        url = reverse('review-update', args=[self.review.id])
        response = self.client.put(url, {'rating': 3, 'review': 'Average'})
        self.assertEqual(response.status_code, 200)
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 3)

    def test_delete_review(self):
        self.client.login(username='buyer', password='buyerpass')
        url = reverse('review-delete', args=[self.review.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_permission_required_for_add(self):
        url = reverse('review-add', args=[self.product.id])
        data = {'rating': 4, 'review': 'Good phone'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)

    def test_permission_required_for_update(self):
        url = reverse('review-update', args=[self.review.id])
        response = self.client.put(url, {'rating': 2, 'review': 'Bad'})
        self.assertEqual(response.status_code, 401)

    def test_permission_required_for_delete(self):
        url = reverse('review-delete', args=[self.review.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    def test_my_products_only_returns_owned_products(self):
        # Create a product for another user
        other_product = Product.objects.create(
            name='Tablet',
            description='A smart tablet',
            price=300.00,
            quantity=3,
            category=self.category,
            seller=self.other_user
        )
        self.client.login(username='buyer', password='buyerpass')
        url = reverse('my-products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        product_ids = [prod['id'] for prod in response.data]
        self.assertIn(self.product.id, product_ids)
        self.assertNotIn(other_product.id, product_ids)
