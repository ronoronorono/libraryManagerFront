# tests/test_custom_user_profile_serializer.py

from rest_framework.test import APITestCase, APIRequestFactory
from library.models import CustomUserProfile
from library.serializers import CustomUserProfileSerializer

class CustomUserProfileSerializerTestCase(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
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
        self.user = CustomUserProfile.objects.create_user(**self.user_attributes)
        self.staff_user = CustomUserProfile.objects.create_user(**self.staff_user_attributes)
        self.superuser = CustomUserProfile.objects.create_user(**self.superuser_attributes)

    def tearDown(self):
        CustomUserProfile.objects.all().delete()

    def test_contains_expected_fields(self):
        serializer = CustomUserProfileSerializer(instance=self.user)
        data = serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'first_name', 'last_name', 'email', 'username', 'library_card_number', 'updated_at', 'is_staff', 'is_superuser']))

    def test_user_serialization(self):
        serializer = CustomUserProfileSerializer(instance=self.user)
        data = serializer.data
        self.assertEqual(data['username'], self.user_attributes['username'])
        self.assertEqual(data['library_card_number'], self.user_attributes['library_card_number'])

    def test_staff_user_serialization(self):
        serializer = CustomUserProfileSerializer(instance=self.staff_user)
        data = serializer.data
        self.assertEqual(data['username'], self.staff_user_attributes['username'])
        self.assertEqual(data['library_card_number'], self.staff_user_attributes['library_card_number'])

    def test_superuser_serialization(self):
        serializer = CustomUserProfileSerializer(instance=self.superuser)
        data = serializer.data
        self.assertEqual(data['username'], self.superuser_attributes['username'])
        self.assertEqual(data['library_card_number'], self.superuser_attributes['library_card_number'])

    def test_valid_user_deserialization(self):
        data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'library_card_number': '89883774',
        }
        request = self.factory.post('/customuserprofile/', data)
        request.user = self.staff_user
        serializer = CustomUserProfileSerializer(data=data, context={'request': request})
        is_valid_user = serializer.is_valid()
        #print(serializer.errors)
        self.assertTrue(is_valid_user)
        user = serializer.save()
        #print(serializer.data)
        self.assertEqual(user.username, data['username'])
        self.assertEqual(user.library_card_number, data['library_card_number'])

    def test_valid_staff_user_deserialization(self):
        data = {
            'username': 'newstaffuser',
            'password': 'newpassword123',
            'library_card_number': '1234509876',
            'is_staff': True
        }
        request = self.factory.post('/customuserprofile/', data)
        request.user = self.staff_user
        serializer = CustomUserProfileSerializer(data=data, context={'request': request})
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, data['username'])
        self.assertEqual(user.library_card_number, data['library_card_number'])
        self.assertTrue(user.is_staff)

    def test_valid_superuser_deserialization(self):
        data = {
            'username': 'newsuperuser',
            'password': 'newpassword123',
            'library_card_number': '9883746657',
            'is_superuser': True
        }
        request = self.factory.post('/customuserprofile/', data)
        request.user = self.staff_user
        serializer = CustomUserProfileSerializer(data=data, context={'request': request})
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
       # print(serializer.data)
        self.assertEqual(user.username, data['username'])
        self.assertEqual(user.library_card_number, data['library_card_number'])
        self.assertTrue(user.is_superuser)

    def test_invalid_deserialization(self):
        data = {
            'username': '',
            'password': 'newpassword123',
            'library_card_number': '0988776666'
        }
        serializer = CustomUserProfileSerializer(data=data)
        valid_serializer = serializer.is_valid()
        self.assertFalse(valid_serializer)
        self.assertEqual(set(serializer.errors.keys()), set(['username']))