# library/tests/bookModel_test.py

from django.test import TestCase
from django.utils import timezone
from library.models.book import Book
from library.models.author import Author
from library.models.categories import Category
from library.models.publisher import Publisher

class BookModelTest(TestCase):

    def setUp(self):
        self.publisher = Publisher.objects.create(publisher_name='Test Publisher')
        self.author1 = Author.objects.create(first_name='John', last_name='Doe', nationality='American')
        self.author2 = Author.objects.create(first_name='Jane', last_name='Smith', nationality='British')
        self.author3 = Author.objects.create(first_name='Jane', last_name='Doe', nationality='Brazilian')
        self.category1 = Category.objects.create(name='Fiction', description='Fictional books')
        self.category2 = Category.objects.create(name='Science', description='Scientific books')
        self.book = Book.objects.create(
            title='Test Book',
            publisher=self.publisher,
            year=2023,
            description='A test book description'
        )
        self.book.author.set([self.author1, self.author2])
        self.book.category.set([self.category1, self.category2])

    def test_create_book(self):
        self.assertEqual(self.book.title, 'Test Book')
        self.assertEqual(self.book.publisher, self.publisher)
        self.assertEqual(self.book.year, 2023)
        self.assertEqual(self.book.description, 'A test book description')
        self.assertTrue(self.book.is_active)
        self.assertIsNone(self.book.deleted_at)
        self.assertEqual(self.book.author.count(), 2)
        self.assertEqual(self.book.category.count(), 2)

    def test_read_book(self):
        book = Book.objects.get(pk=self.book.pk)
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.publisher, self.publisher)
        self.assertEqual(book.author.count(), 2)
        self.assertEqual(book.category.count(), 2)

    def test_update_book(self):
        self.book.title = 'Updated Test Book'
        self.book.save()
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Test Book')

    def test_soft_delete_book(self):
        self.book.delete()
        self.book.refresh_from_db()
        self.assertFalse(self.book.is_active)
        self.assertIsNotNone(self.book.deleted_at)

    def test_hard_delete_book(self):
        self.book.is_active = False
        self.book.deleted_at = timezone.now()
        self.book.save()
        self.book.delete()
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(pk=self.book.pk)

    def test_add_multiple_authors(self):
        author3 = Author.objects.create(first_name='Alice', last_name='Johnson', nationality='Canadian')
        self.book.author.add(author3)
        self.assertEqual(self.book.author.count(), 3)

    def test_add_multiple_categories(self):
        category3 = Category.objects.create(name='History', description='Historical books')
        self.book.category.add(category3)
        self.assertEqual(self.book.category.count(), 3)