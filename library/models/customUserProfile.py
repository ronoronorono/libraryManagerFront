from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, ContentType

class CustomUserProfile(AbstractUser):

    library_card_number = models.CharField(max_length=50, unique=True, blank=True, null=True, default=None)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.is_superuser:
            return

        group_name = 'staff' if self.is_staff else 'user'
        group, created = Group.objects.get_or_create(name=group_name)

        if created:
            user_content_type = ContentType.objects.get_for_model(CustomUserProfile)
            group_content_type = ContentType.objects.get_for_model(Group)

            if group_name == 'staff':
                permissions = [
                    Permission.objects.get_or_create(codename='add_user', name='Can add user',
                                                     content_type=user_content_type)[0],
                    Permission.objects.get_or_create(codename='change_user', name='Can change user',
                                                     content_type=user_content_type)[0],
                    Permission.objects.get_or_create(codename='delete_user', name='Can delete user',
                                                     content_type=user_content_type)[0],
                    Permission.objects.get_or_create(codename='view_user', name='Can view user',
                                                     content_type=user_content_type)[0],
                    Permission.objects.get_or_create(codename='add_group', name='Can add group',
                                                     content_type=group_content_type)[0],
                    Permission.objects.get_or_create(codename='change_group', name='Can change group',
                                                     content_type=group_content_type)[0],
                    Permission.objects.get_or_create(codename='delete_group', name='Can delete group',
                                                     content_type=group_content_type)[0],
                    Permission.objects.get_or_create(codename='view_group', name='Can view group',
                                                     content_type=group_content_type)[0],
                ]
                #permissions = Permission.objects.filter(codename__in=['add_user', 'change_user', 'delete_user', 'view_user',
                #                                                      'add_group', 'change_group', 'delete_group', 'view_group',])
                group.permissions.set(permissions)
                self.is_staff = True
            else:
                permissions = [
                    Permission.objects.get_or_create(codename='view_user', name='Can view user',
                                                     content_type=user_content_type)[0],
                    Permission.objects.get_or_create(codename='view_group', name='Can view group',
                                                     content_type=group_content_type)[0],
                ]
                self.is_staff = False
                #permissions = Permission.objects.filter(codename__in=['view_user', 'view_group'])
                group.permissions.set(permissions)

        if not self.groups.filter(name=group_name).exists():
            self.groups.add(group)
            self.save()