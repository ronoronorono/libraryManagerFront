# library/tests/authorModel_test.py

from django.test import TestCase
from django.utils import timezone
from library.models.author import Author

class AuthorModelTest(TestCase):

    def setUp(self):
        self.author = Author.objects.create(
            first_name='John',
            last_name='Doe',
            nationality='American'
        )

    def test_create_author(self):
        self.assertEqual(self.author.first_name, 'John')
        self.assertEqual(self.author.last_name, 'Doe')
        self.assertEqual(self.author.nationality, 'American')
        self.assertTrue(self.author.is_active)
        self.assertIsNone(self.author.deleted_at)

    def test_read_author(self):
        author = Author.objects.get(pk=self.author.pk)
        self.assertEqual(author.first_name, 'John')
        self.assertEqual(author.last_name, 'Doe')

    def test_update_author(self):
        self.author.first_name = 'Jane'
        self.author.save()
        self.author.refresh_from_db()
        self.assertEqual(self.author.first_name, 'Jane')

    def test_delete_author(self):
        self.author.is_active = False
        self.author.save()
        self.author.delete()
        with self.assertRaises(Author.DoesNotExist):
            Author.objects.get(pk=self.author.pk)

    def test_soft_delete_author(self):
        self.author.delete()
        self.author.refresh_from_db()
        self.assertFalse(self.author.is_active)
        self.assertIsNotNone(self.author.deleted_at)

    def test_hard_delete_author(self):
        self.author.is_active = False
        self.author.deleted_at = timezone.now()
        self.author.save()
        self.author.delete()
        with self.assertRaises(Author.DoesNotExist):
            Author.objects.get(pk=self.author.pk)

    def test_blank_first_name(self):
        self.author.first_name = ''
        self.assertRaises(Exception)
        self.author.save()

    def test_blank_last_name(self):
        self.author.last_name = ''
        self.assertRaises(Exception)
        self.author.save()

    def test_str_method(self):
        self.assertEqual(str(self.author), 'John Doe')