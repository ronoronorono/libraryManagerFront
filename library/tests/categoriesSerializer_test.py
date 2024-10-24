# library/tests/categoriesSerializer_test.py

from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.exceptions import ValidationError
from library.models import Category
from library.serializers.categoriesSerializer import categoriesSerializer

class CategorySerializerTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.category_data = {
            'name': 'Test Category',
            'description': 'A test category'
        }
        self.category = Category.objects.create(**self.category_data)

    def test_valid_category_serializer(self):
        serializer = categoriesSerializer(instance=self.category)
        self.assertEqual(serializer.data['name'], self.category_data['name'])
        self.assertEqual(serializer.data['description'], self.category_data['description'])

    def test_create_category_serializer(self):
        data = {
            'name': 'New Category',
            'description': 'A new category'
        }

        serializer = categoriesSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        category = serializer.save()
        self.assertEqual(category.name, data['name'])
        self.assertEqual(category.description, data['description'])

    def test_update_category_serializer(self):
        data = {
            'name': 'Updated Category',
            'description': 'An updated category'
        }
        serializer = categoriesSerializer(instance=self.category, data=data)
        self.assertTrue(serializer.is_valid())
        category = serializer.save()
        self.assertEqual(category.name, data['name'])
        self.assertEqual(category.description, data['description'])

    def test_invalid_category_serializer(self):
        data = {
            'name': '',
            'description': 'An invalid category'
        }
        serializer = categoriesSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_partial_update_category_serializer(self):
        data = {
            'description': 'A partially updated category'
        }
        serializer = categoriesSerializer(instance=self.category, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        category = serializer.save()
        self.assertEqual(category.name, self.category_data['name'])
        self.assertEqual(category.description, data['description'])