# library/tests/authorSerializer_test.py

from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError
from library.models.author import Author
from library.serializers.authorSerializer import AuthorSerializer
from django.utils import timezone

class AuthorSerializerTest(APITestCase):

    def setUp(self):
        self.author_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'nationality': 'American'
        }
        self.author = Author.objects.create(**self.author_data)

    def test_valid_author_serializer(self):
        serializer = AuthorSerializer(instance=self.author)
        self.assertEqual(serializer.data['first_name'], self.author_data['first_name'])
        self.assertEqual(serializer.data['last_name'], self.author_data['last_name'])
        self.assertEqual(serializer.data['nationality'], self.author_data['nationality'])

    def test_create_author_serializer(self):
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'nationality': 'British'
        }
        serializer = AuthorSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        author = serializer.save()
        self.assertEqual(author.first_name, data['first_name'])
        self.assertEqual(author.last_name, data['last_name'])
        self.assertEqual(author.nationality, data['nationality'])

    def test_update_author_serializer(self):
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe'
        }
        serializer = AuthorSerializer(instance=self.author, data=data)
        self.assertTrue(serializer.is_valid())
        author = serializer.save()
        self.assertEqual(author.first_name, data['first_name'])
        self.assertEqual(author.last_name, data['last_name'])

    def test_soft_delete_author(self):
        self.author.is_active = False
        self.author.deleted_at = timezone.now()
        self.author.save()
        serializer = AuthorSerializer(instance=self.author)
        self.assertFalse(serializer.data['is_active'])
        self.assertIsNotNone(serializer.data['deleted_at'])

    def test_hard_delete_author(self):
        self.author.is_active = False
        self.author.deleted_at = timezone.now()
        self.author.save()
        self.author.delete()
        with self.assertRaises(Author.DoesNotExist):
            Author.objects.get(pk=self.author.pk)

    def test_blank_first_name(self):
        data = {
            'first_name': '',
            'last_name': 'Doe'
        }
        serializer = AuthorSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_blank_last_name(self):
        data = {
            'first_name': 'John',
            'last_name': ''
        }
        serializer = AuthorSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_unauthorized_field_change(self):
        data = {
            'id': 999,
            'first_name': '',
            'last_name': 'Change'
        }
        serializer = AuthorSerializer(instance=self.author, data=data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)