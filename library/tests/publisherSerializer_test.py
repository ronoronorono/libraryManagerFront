# library/tests/publisherSerializer_test.py

from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError
from library.models import Publisher
from library.serializers.publisherSerializer import publisherSerializer
from django.utils import timezone

class PublisherSerializerTest(APITestCase):

    def setUp(self):
        self.publisher_data = {
            'publisher_name': 'Test Publisher'
        }
        self.publisher = Publisher.objects.create(**self.publisher_data)

    def test_valid_publisher_serializer(self):
        serializer = publisherSerializer(instance=self.publisher)
        self.assertEqual(serializer.data['publisher_name'], self.publisher_data['publisher_name'])

    def test_create_publisher_serializer(self):
        data = {
            'publisher_name': 'New Publisher'
        }
        serializer = publisherSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        publisher = serializer.save()
        self.assertEqual(publisher.publisher_name, data['publisher_name'])

    def test_update_publisher_serializer(self):
        data = {
            'publisher_name': 'Updated Publisher'
        }
        serializer = publisherSerializer(instance=self.publisher, data=data)
        self.assertTrue(serializer.is_valid())
        publisher = serializer.save()
        self.assertEqual(publisher.publisher_name, data['publisher_name'])

    def test_soft_delete_publisher(self):
        self.publisher.is_active = False
        self.publisher.deleted_at = timezone.now()
        self.publisher.save()
        serializer = publisherSerializer(instance=self.publisher)
        self.assertFalse(serializer.data['is_active'])
        self.assertIsNotNone(serializer.data['deleted_at'])

    def test_hard_delete_publisher(self):
        self.publisher.is_active = False
        self.publisher.deleted_at = timezone.now()
        self.publisher.save()
        self.publisher.delete()
        with self.assertRaises(Publisher.DoesNotExist):
            Publisher.objects.get(pk=self.publisher.pk)

    def test_blank_field(self):
        data = {
            'publisher_name': ''
        }
        serializer = publisherSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
    #
    # def test_unauthorized_field_change(self):
    #     data = {
    #         'id': 999,
    #         'publisher_name': 'Unauthorized Change'
    #     }
    #     serializer = publisherSerializer(instance=self.publisher, data=data)
    #     self.assertFalse(serializer.is_valid())
    #     with self.assertRaises(ValidationError):
    #         serializer.is_valid(raise_exception=True)