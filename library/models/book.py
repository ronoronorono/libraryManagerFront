from django.db import models
from django.utils import timezone

from .author import Author
from .categories import Category

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, unique=False)
    author = models.ManyToManyField(Author, related_name='author')
    category = models.ManyToManyField(Category, related_name='categories')
    publisher = models.ForeignKey('Publisher', on_delete=models.RESTRICT)
    year = models.PositiveBigIntegerField()
    description = models.TextField(blank=True, null=True, default=None)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)
    #book_copies = models.ForeignKey('BookCopies', on_delete=models.RESTRICT, related_name='book_copies',default=None)

    def __str__(self):
        return f'{self.title} - {self.author} - {self.year}'

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