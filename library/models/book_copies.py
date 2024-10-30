from django.db import models
from django.utils import timezone

from .book import Book

class BookCopies(models.Model):

    class BookStatus(models.TextChoices):
        AVAILABLE = 'Available'
        BORROWED = 'Borrowed'
        RESERVED = 'Reserved'
        LOST = 'Lost'
        UNAVAILABLE = 'Unavailable',
        INTERNAL_USE = 'Internal Use'

    #id = models.AutoField(primary_key=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, unique=False, related_name='book', related_query_name='books', default=None)
    status = models.CharField(max_length=50, choices=BookStatus.choices, default=BookStatus.AVAILABLE)

