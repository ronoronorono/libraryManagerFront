# library/tests/publisherView_test.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from library.models import Publisher
from library.serializers.publisherSerializer import publisherSerializer
from library.models.customUserProfile import CustomUserProfile

class PublisherViewSetTest(APITestCase):

    def setUp(self):
        self.publisher_data = {
            'publisher_name': 'Test Publisher'
        }
        self.publisher = Publisher.objects.create(**self.publisher_data)
        self.token_url = reverse('token_obtain_pair')
        self.staff_user_attributes = {
            'username': 'staffuser',
            'password': 'password123',
            'is_staff': True
        }
        self.non_staff_user_attributes = {
            'username': 'nonstaffuser',
            'password': 'password123',
            'is_staff': False
        }
        self.staff_user = CustomUserProfile.objects.create_user(**self.staff_user_attributes)
        self.non_staff_user = CustomUserProfile.objects.create_user(**self.non_staff_user_attributes)

    def get_jwt_token(self, user_attributes):
        response = self.client.post(self.token_url, data=user_attributes)
        return response.data['access']

    def set_credentials(self, user_attributes):
        token = self.get_jwt_token(user_attributes)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def create_more_publishers(self, number_of_publishers):
        publishers = [
            Publisher(
                publisher_name=f'Publisher{i}'
            )
            for i in range(number_of_publishers)
        ]
        Publisher.objects.bulk_create(publishers)

    def test_create_more_than_5000_publishers(self):
        self.set_credentials(self.staff_user_attributes)
        self.create_more_publishers(5000)
        response = self.client.get(reverse('library:publishers-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(response.data['registers'], 5001)  # Including the initial publisher

    def test_list_publishers(self):
        self.set_credentials(self.staff_user_attributes)
        response = self.client.get(reverse('library:publishers-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_publishers_by_user(self):
        self.set_credentials(self.non_staff_user_attributes)
        response = self.client.get(reverse('library:publishers-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_publisher(self):
        self.set_credentials(self.staff_user_attributes)
        response = self.client.get(reverse('library:publishers-detail', args=[self.publisher.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['publisher_name'], self.publisher_data['publisher_name'])

    def test_retrieve_publisher_by_user(self):
        self.set_credentials(self.non_staff_user_attributes)
        response = self.client.get(reverse('library:publishers-detail', args=[self.publisher.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_publisher(self):
        self.set_credentials(self.staff_user_attributes)
        data = {
            'publisher_name': 'New Publisher'
        }
        response = self.client.post(reverse('library:publishers-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Publisher.objects.count(), 2)

    def test_create_publisher_by_user(self):
        self.set_credentials(self.non_staff_user_attributes)
        data = {
            'publisher_name': 'New Publisher'
        }
        print(self.non_staff_user_attributes)
        response = self.client.post(reverse('library:publishers-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_update_publisher(self):
        self.set_credentials(self.staff_user_attributes)
        data = {
            'publisher_name': 'Updated Publisher'
        }
        response = self.client.put(reverse('library:publishers-detail', args=[self.publisher.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.publisher.refresh_from_db()
        self.assertEqual(self.publisher.publisher_name, data['publisher_name'])

    def test_partial_update_publisher(self):
        self.set_credentials(self.staff_user_attributes)
        data = {
            'publisher_name': 'Partially Updated Publisher'
        }
        response = self.client.patch(reverse('library:publishers-detail', args=[self.publisher.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.publisher.refresh_from_db()
        self.assertEqual(self.publisher.publisher_name, data['publisher_name'])

    def test_delete_publisher(self):
        self.set_credentials(self.staff_user_attributes)
        self.publisher.is_active = False
        self.publisher.deleted_at = timezone.now()
        self.publisher.save()
        response = self.client.delete(reverse('library:publishers-detail', args=[self.publisher.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Publisher.objects.filter(pk=self.publisher.pk).exists())

    def test_soft_delete_publisher(self):
        self.set_credentials(self.staff_user_attributes)
        self.publisher.is_active = False
        self.publisher.deleted_at = timezone.now()
        self.publisher.save()
        response = self.client.get(reverse('library:publishers-detail', args=[self.publisher.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_active'])
        self.assertIsNotNone(response.data['deleted_at'])

    def test_hard_delete_publisher(self):
        self.set_credentials(self.staff_user_attributes)
        self.publisher.is_active = False
        self.publisher.deleted_at = timezone.now()
        self.publisher.save()
        self.publisher.delete()
        with self.assertRaises(Publisher.DoesNotExist):
            Publisher.objects.get(pk=self.publisher.pk)

    def test_filter_publishers(self):
        self.set_credentials(self.staff_user_attributes)
        response = self.client.get(reverse('library:publishers-list'), {'publisher_name': 'Test Publisher'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['registers'], 1)

    def test_pagination(self):
        self.set_credentials(self.staff_user_attributes)
        self.create_more_publishers(5000)
        response = self.client.get(reverse('library:publishers-list'), {'page': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data)

    def test_non_staff_user_permissions(self):
        self.set_credentials(self.non_staff_user_attributes)
        data = {
            'publisher_name': 'Unauthorized Publisher'
        }
        response = self.client.post(reverse('library:publishers-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)