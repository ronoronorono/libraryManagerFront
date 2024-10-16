from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from library.models import CustomUserProfile

class CustomUserProfileTestCase(TestCase):

    def setUp(self):
        self.user = CustomUserProfile.objects.create_user(username='test', password='test')
        self.staff_user = CustomUserProfile.objects.create_user(username='staff', password='staff', is_staff=True)

    def test_user_group_assigment(self):
        self.user.save()
        user_group = Group.objects.get(name='user')
        self.assertIn(user_group, self.user.groups.all())

    def test_staff_group_assigment(self):
        self.staff_user.save()
        staff_group = Group.objects.get(name='staff')
        self.assertIn(staff_group, self.staff_user.groups.all())

    def test_user_permissions_assignment(self):
        self.user.save()
        user_group = Group.objects.get(name='user')
        view_permission = Permission.objects.get(codename='view_user')
        self.assertIn(view_permission, user_group.permissions.all())

    def test_staff_permissions_assignment(self):
        self.staff_user.save()
        staff_group = Group.objects.get(name='staff')
        add_permission = Permission.objects.get(codename='add_user')
        change_permission = Permission.objects.get(codename='change_user')
        delete_permission = Permission.objects.get(codename='delete_user')
        view_permission = Permission.objects.get(codename='view_user')
        self.assertIn(add_permission, staff_group.permissions.all())
        self.assertIn(change_permission, staff_group.permissions.all())
        self.assertIn(delete_permission, staff_group.permissions.all())
        self.assertIn(view_permission, staff_group.permissions.all())