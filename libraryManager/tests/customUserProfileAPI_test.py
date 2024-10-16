from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from library.models import CustomUserProfile

class CustomUserProfileAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUserProfile.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com'
        )
        self.staff_user = CustomUserProfile.objects.create_user(
            username='staffuser',
            password='staffpassword',
            email='staffuser@example.com',
            is_staff=True
        )
        self.superuser = CustomUserProfile.objects.create_superuser(
            username='superuser',
            password='superpassword',
            email='superuser@example.com'
        )
        self.login_url = reverse('token_obtain_pair')
        self.profile_url = reverse('library:customuserprofile-list')

    def authenticate(self, username, password):
        response = self.client.post(self.login_url, {'username': username, 'password': password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])

    def test_crud_operations_normal_user(self):
        # Authenticate as normal user
        self.authenticate('testuser', 'testpassword')

        # Normal user should not be able to create a new user profile
        create_data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(self.profile_url, create_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_crud_operations_staff_user(self):
        # Authenticate as staff user
        self.authenticate('staffuser', 'staffpassword')

        # Create a new user profile
        create_data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(self.profile_url, create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_id = response.data['id']

        # Retrieve the user profile
        response = self.client.get(reverse('library:customuserprofile-detail', args=[user_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], create_data['username'])

        # Update the user profile
        update_data = {
            'first_name': 'Updated',
            'last_name': 'User'
        }
        response = self.client.patch(reverse('library:customuserprofile-detail', args=[user_id]), update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], update_data['first_name'])

        # Delete the user profile
        response = self.client.delete(reverse('library:customuserprofile-detail', args=[user_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the user profile is deleted
        response = self.client.get(reverse('library:customuserprofile-detail', args=[user_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_crud_operations_superuser(self):
        # Authenticate as superuser
        self.authenticate('superuser', 'superpassword')

        # Create a new user profile
        create_data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(self.profile_url, create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_id = response.data['id']

        # Retrieve the user profile
        response = self.client.get(reverse('library:customuserprofile-detail', args=[user_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], create_data['username'])

        # Update the user profile
        update_data = {
            'first_name': 'Updated',
            'last_name': 'User'
        }
        response = self.client.patch(reverse('library:customuserprofile-detail', args=[user_id]), update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], update_data['first_name'])

        # Delete the user profile
        response = self.client.delete(reverse('library:customuserprofile-detail', args=[user_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the user profile is deleted
        response = self.client.get(reverse('library:customuserprofile-detail', args=[user_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)