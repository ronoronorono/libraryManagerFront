from django.db import models
from django.utils import timezone

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True, default=None)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):

        if not self.is_active and self.deleted_at is not None:
            models.Model.delete(self, *args, **kwargs)
        else:
            self.is_active = False
            self.deleted_at = timezone.now()
            self.save()

    def save(self, *args, **kwargs):
        #super().save(*args, **kwargs)

        if self.is_active:
            self.is_active = True
            self.deleted_at = None
        else:
            self.is_active = False
            self.deleted_at = timezone.now()

        super().save(*args, **kwargs)

