# library/tests/categoriesViews_test.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from library.models import Category, CustomUserProfile
from library.serializers.categoriesSerializer import categoriesSerializer

class CategoriesViewSetTest(APITestCase):

    def setUp(self):
        self.category_data = {
            'name': 'Test Category',
            'description': 'A test category'
        }
        self.category = Category.objects.create(**self.category_data)
        self.token_url = reverse('token_obtain_pair')
        self.staff_user_attributes = {
            'username': 'staffuser',
            'password': 'password123',
            'is_staff': True
        }
        self.staff_user = CustomUserProfile.objects.create_user(**self.staff_user_attributes)

    def get_jwt_token(self, user_attributes):
        response = self.client.post(self.token_url, data=user_attributes)
        return response.data['access']

    def set_credentials(self, user_attributes):
        token = self.get_jwt_token(user_attributes)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def create_more_categories(self, number_of_categories):
        categories = [
            Category(
                name=f'Category{i}',
                description=f'Description for category {i}'
            )
            for i in range(number_of_categories)
        ]
        Category.objects.bulk_create(categories)

    def test_create_more_than_5000_categories(self):
        self.set_credentials(self.staff_user_attributes)
        self.create_more_categories(5000)
        response = self.client.get(reverse('library:categories-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['registers'], 5001)  # Including the initial category

    def test_list_categories(self):
        self.set_credentials(self.staff_user_attributes)
        response = self.client.get(reverse('library:categories-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_category(self):
        self.set_credentials(self.staff_user_attributes)
        response = self.client.get(reverse('library:categories-detail', args=[self.category.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.category_data['name'])

    def test_create_category(self):
        self.set_credentials(self.staff_user_attributes)
        data = {
            'name': 'New Category',
            'description': 'A new category'
        }
        response = self.client.post(reverse('library:categories-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_update_category(self):
        self.set_credentials(self.staff_user_attributes)
        data = {
            'name': 'Updated Category',
            'description': 'An updated category'
        }
        response = self.client.put(reverse('library:categories-detail', args=[self.category.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, data['name'])

    def test_partial_update_category(self):
        self.set_credentials(self.staff_user_attributes)
        data = {
            'description': 'A partially updated category'
        }
        response = self.client.patch(reverse('library:categories-detail', args=[self.category.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.description, data['description'])

    def test_delete_category(self):
        self.set_credentials(self.staff_user_attributes)
        print(self.category.pk)
        response = self.client.delete(reverse('library:categories-detail', args=[self.category.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(pk=self.category.pk).first().is_active)