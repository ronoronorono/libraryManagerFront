# tests/test_custom_user_profile_view.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from library.models import CustomUserProfile

class CustomUserProfileViewTestCase(APITestCase):

    def setUp(self):
        self.user_attributes = {
            'username': 'testuser',
            'password': 'password123',
            'library_card_number': '1234567890'
        }
        self.staff_user_attributes = {
            'username': 'staffuser',
            'password': 'password123',
            'library_card_number': '0987654321',
            'is_staff': True
        }
        self.superuser_attributes = {
            'username': 'superuser',
            'password': 'password123',
            'library_card_number': '1122334455',
            'is_superuser': True
        }

        # Ensure library_card_number is unique
        assert not CustomUserProfile.objects.filter(library_card_number=self.user_attributes['library_card_number']).exists()
        assert not CustomUserProfile.objects.filter(library_card_number=self.staff_user_attributes['library_card_number']).exists()
        assert not CustomUserProfile.objects.filter(library_card_number=self.superuser_attributes['library_card_number']).exists()

        self.user = CustomUserProfile.objects.create_user(**self.user_attributes)
        self.staff_user = CustomUserProfile.objects.create_user(**self.staff_user_attributes)
        self.superuser = CustomUserProfile.objects.create_user(**self.superuser_attributes)
        self.token_url = reverse('token_obtain_pair')

    def tearDown(self):
        CustomUserProfile.objects.all().delete()

    def get_jwt_token(self, user_attributes):
        response = self.client.post(self.token_url, data=user_attributes)
        return response.data['access']

    def test_list_users_as_staff(self):
        token = self.get_jwt_token(self.staff_user_attributes)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(reverse('library:customuserprofile-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_users_as_normal_user(self):
        token = self.get_jwt_token(self.user_attributes)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(reverse('library:customuserprofile-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user_as_staff(self):
        token = self.get_jwt_token(self.staff_user_attributes)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(reverse('library:customuserprofile-detail', args=[self.user.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_own_profile_as_user(self):
        token = self.get_jwt_token(self.user_attributes)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(reverse('library:customuserprofile-detail', args=[self.user.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_other_profile_as_user(self):
        token = self.get_jwt_token(self.user_attributes)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(reverse('library:customuserprofile-detail', args=[self.staff_user.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_as_staff(self):
        token = self.get_jwt_token(self.staff_user_attributes)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'library_card_number': '987774621'
        }
        response = self.client.post(reverse('library:customuserprofile-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_as_normal_user(self):
        token = self.get_jwt_token(self.user_attributes)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'library_card_number': '76538847'
        }
        response = self.client.post(reverse('library:customuserprofile-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_as_staff(self):
        token = self.get_jwt_token(self.staff_user_attributes)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        data = {
            'username': 'updateduser',
            'library_card_number': '1234509876'
        }
        response = self.client.patch(reverse('library:customuserprofile-detail', args=[self.user.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_own_profile_as_user(self):
        token = self.get_jwt_token(self.user_attributes)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        data = {
            'first_name': 'updateduser',
            'last_name': 'updateduser_lastname',
            'email': 'test@test.com'
        }
        response = self.client.patch(reverse('library:customuserprofile-detail', args=[self.user.pk]), data)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_other_profile_as_user(self):
        token = self.get_jwt_token(self.user_attributes)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        data = {
            'username': 'updateduser',
            'library_card_number': '1234509876'
        }
        response = self.client.patch(reverse('library:customuserprofile-detail', args=[self.staff_user.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_as_staff(self):
        token = self.get_jwt_token(self.staff_user_attributes)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.delete(reverse('library:customuserprofile-detail', args=[self.user.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_as_normal_user(self):
        token = self.get_jwt_token(self.user_attributes)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.delete(reverse('library:customuserprofile-detail', args=[self.user.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)