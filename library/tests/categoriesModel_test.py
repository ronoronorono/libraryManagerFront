# library/tests/categoriesModel_test.py

from django.test import TestCase
from django.utils import timezone
from library.models.categories import Category

class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            description='A test category'
        )

    def test_create_category(self):
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(self.category.description, 'A test category')
        self.assertTrue(self.category.is_active)
        self.assertIsNone(self.category.deleted_at)

    def test_soft_delete_category(self):
        self.category.delete()
        self.category.refresh_from_db()
        self.assertFalse(self.category.is_active)
        self.assertIsNotNone(self.category.deleted_at)

    def test_hard_delete_category(self):
        self.category.is_active = False
        self.category.deleted_at = timezone.now()
        self.category.save()
        self.category.delete()
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(pk=self.category.pk)

    def test_reactivate_category(self):
        self.category.delete()
        self.category.is_active = True
        self.category.deleted_at = None
        self.category.save()
        self.category.refresh_from_db()
        self.assertTrue(self.category.is_active)
        self.assertIsNone(self.category.deleted_at)

    def test_update_category(self):
        self.category.name = 'Updated Category'
        self.category.save()
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Category')

    def test_str_method(self):
        self.assertEqual(str(self.category), 'Test Category')