from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User
import json


# Create your tests here.
class AuthenticationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        self.admin = User.objects.create_user(username='adminuser', email='admin@example.com', password='adminpass', role='admin', is_staff=True)

    def test_valid_login(self):
        """Check if users can login with valid credentials"""
        # URL for endpoint
        url = reverse('login')

        # Data to be sent in the request
        data = {
            'username': 'testuser',
            'password': 'testpass'
            }
        
        # Make a request to the endpoint
        response = self.client.post(url, data)

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the expected data
        self.assertIn('Login successful', response.data['message'])

    def test_invalid_login(self):
        """Check if users cannot login with invalid credentials"""
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'wrongpass'
            }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid credentials', response.data['detail'])

    def test_valid_register(self):
        """Check if users can register with valid credentials"""
        url = reverse('register')
        data = {
            'username': 'mazen',
            'email': 'mazen@example.com',
            'password': 'mazen123',
            'confirmation': 'mazen123'
            }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Registration successful', response.data['message'])

    def test_wrong_confirmation(self):
        """Check if users cannot register with mismatched passwords"""
        url = reverse('register')
        data = {
            'username': 'uniqueuserforconfirmation',
            'email': 'uniqueuserforconfirmation@example.com',
            'password': 'testpass',
            'confirmation': 'wrongconfirmation'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.data)
        self.assertIn('Passwords must match.', response.data['password'][0])

    def test_username_taken(self):
        """Check if users cannot register with an already taken username"""
        url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass',
            'confirmation': 'testpass'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('username', response.data)
        self.assertTrue(any('already exists' in err or 'already taken' in err for err in response.data['username']))

    def test_logout(self):
        """Check if users can logout"""
        # First login to get authenticated
        self.client.login(username='testuser', password='testpass')
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        # Check if the user is logged out by trying to access a protected view
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, 401)

class UserEndpointsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', email='user1@example.com', password='userpass')
        self.admin = User.objects.create_user(username='admin1', email='admin1@example.com', password='adminpass', role='admin', is_staff=True)

    def test_user_profile(self):
        """Check if users can get their profile"""
        self.client.login(username='user1', password='userpass')
        url = reverse('user-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'user1')

    def test_activate_account(self):
        """Check if users can activate their account"""
        self.client.login(username='user1', password='userpass')
        url = reverse('user-activate')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.isVerified)

    def test_update_profile_image(self):
        """Check if users can update their profile image"""
        self.client.login(username='user1', password='userpass')
        url = reverse('user-update-image')
        response = self.client.post(url, {'profileImage': 'newimage.jpg'})
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.profileImage, 'newimage.jpg')

    def test_update_profile_image_invalid_type(self):
        """Should fail if image type is not jpg, jpeg, or png"""
        self.client.login(username='user1', password='userpass')
        url = reverse('user-update-image')
        response = self.client.post(url, {'profileImage': 'image.bmp'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid image type', response.data['detail'])

    def test_update_profile_image_valid_base64(self):
        """Should succeed with a valid small base64 png image string"""
        self.client.login(username='user1', password='userpass')
        url = reverse('user-update-image')
        # Small valid base64 string for a png
        fake_data = 'data:image/png;base64,' + ('A' * 100)
        response = self.client.post(url, {'profileImage': fake_data})
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.profileImage, fake_data)

    def test_get_current_user(self):
        """Check if users can get their current user"""
        self.client.login(username='user1', password='userpass')
        url = reverse('user-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'user1')

    def test_deactivate_account(self):
        """Check if users can deactivate their account"""
        self.client.login(username='user1', password='userpass')
        url = reverse('user-deactivate')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertFalse(self.user.IsActive)

    def test_admin_change_password(self):
        """Check if admins can change user passwords"""
        self.client.login(username='admin1', password='adminpass')
        url = reverse('admin-change-password', args=[self.user.id])
        response = self.client.post(url, {'password': 'newpass123'})
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass123'))

    def test_admin_create_user(self):
        """Check if admins can create users"""
        self.client.login(username='admin1', password='adminpass')
        url = reverse('admin-create')
        data = {'username': 'newadmin', 'email': 'newadmin@example.com', 'password': 'admin123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username='newadmin').exists())

    def test_admin_get_user(self):
        """Check if admins can get users"""
        self.client.login(username='admin1', password='adminpass')
        url = reverse('admin-get', args=[self.admin.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'admin1')

    def test_admin_delete_user(self):
        """Check if admins can delete users"""
        self.client.login(username='admin1', password='adminpass')
        url = reverse('admin-delete', args=[self.admin.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(id=self.admin.id).exists())

    def test_admin_update_user(self):
        """Check if admins can update users"""
        self.client.login(username='admin1', password='adminpass')
        url = reverse('admin-update', args=[self.admin.id])
        response = self.client.patch(
            url,
            json.dumps({'email': 'updated@example.com'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.email, 'updated@example.com')