from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Replace with your actual URL pattern name
        self.register_url = reverse('register')

        # Test user data
        self.valid_user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
        }

    def test_register_valid_user(self):
        response = self.client.post(
            self.register_url, self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that a new user was created
        self.assertEqual(User.objects.count(), 1)
        # Check the username of the created user
        self.assertEqual(User.objects.get().username, 'newuser')

    def test_register_existing_user(self):
        # Create a user with the same username or email to simulate an existing user
        User.objects.create_user(
            username='newuser', email='newuser@example.com', password='newpassword')

        response = self.client.post(
            self.register_url, self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_418_IM_A_TEAPOT)
        # Check for validation error messages
        self.assertIn('username', response.data['message'])

    def test_register_missing_data(self):
        # Test registration with missing required fields (username, email, password)
        response = self.client.post(self.register_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_418_IM_A_TEAPOT)
        # Check for validation error messages
        self.assertIn('username', response.data['message'])
        self.assertIn('email', response.data['message'])
        self.assertIn('password', response.data['message'])
