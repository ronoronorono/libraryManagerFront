# library/tests/publisherModel_test.py

from django.test import TestCase
from django.utils import timezone
from library.models.publisher import Publisher

class PublisherModelTest(TestCase):

    def setUp(self):
        self.publisher = Publisher.objects.create(
            publisher_name='Test Publisher'
        )

    def test_create_publisher(self):
        self.assertEqual(self.publisher.publisher_name, 'Test Publisher')
        self.assertTrue(self.publisher.is_active)
        self.assertIsNone(self.publisher.deleted_at)

    def test_soft_delete_publisher(self):
        self.publisher.delete()
        self.publisher.refresh_from_db()
        self.assertFalse(self.publisher.is_active)
        self.assertIsNotNone(self.publisher.deleted_at)

    def test_hard_delete_publisher(self):
        self.publisher.is_active = False
        self.publisher.deleted_at = timezone.now()
        self.publisher.save()
        self.publisher.delete()
        with self.assertRaises(Publisher.DoesNotExist):
            Publisher.objects.get(pk=self.publisher.pk)

    def test_reactivate_publisher(self):
        self.publisher.delete()
        self.publisher.is_active = True
        self.publisher.deleted_at = None
        self.publisher.save()
        self.publisher.refresh_from_db()
        self.assertTrue(self.publisher.is_active)
        self.assertIsNone(self.publisher.deleted_at)

    def test_update_publisher(self):
        self.publisher.publisher_name = 'Updated Publisher'
        self.publisher.save()
        self.publisher.refresh_from_db()
        self.assertEqual(self.publisher.publisher_name, 'Updated Publisher')

    def test_str_method(self):
        self.assertEqual(str(self.publisher), 'Test Publisher')