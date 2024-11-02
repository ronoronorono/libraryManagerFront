# library/tests/bookSerializer_test.py

from django.test import TestCase
from rest_framework.exceptions import ValidationError
from library.models import Book, Author, Publisher, Category, BookCopies
from library.serializers import BookSerializer, BookCopiesSerializer
import random

class BookSerializerTest(TestCase):

    def setUp(self):
        # Create 10 authors
        self.authors = [
            Author.objects.create(first_name=f'Author{i}', last_name=f'LastName{i}', nationality=f'Nationality{i}')
            for i in range(10)
        ]

        # Create 15 publishers
        self.publishers = [
            Publisher.objects.create(publisher_name=f'Publisher{i}')
            for i in range(15)
        ]

        # Create 30 categories
        self.categories = [
            Category.objects.create(name=f'Category{i}', description=f'Description{i}')
            for i in range(30)
        ]

    def create_book_data(self, title, publisher, authors, categories, copies):
        return {
            'title': title,
            'publisher': publisher.id,
            'year': 2023,
            'description': f'Description of {title}',
            'author': [author.id for author in authors],
            'category': [category.id for category in categories],
            'book_copies': copies
        }

    def create_book_copies_data(self, num_copies, statuses):
        return [
            {'status': random.choice(statuses)}
            for _ in range(num_copies)
        ]
    def test_create_book_with_copies(self):
        book_data = self.create_book_data(
            'Test Book',
            random.choice(self.publishers),
            random.sample(self.authors, k=3),
            random.sample(self.categories, k=3),
            self.create_book_copies_data(10, [status[0] for status in BookCopies.BookStatus.choices if status[0] != 'Available'])
        )
        # Remove 'book_copies' from book_data before passing it to the serializer
        #book_copies_data = book_data.pop('book_copies')
        serializer = BookSerializer(data=book_data)
        print(serializer.is_valid())
        print(serializer.errors)
        self.assertTrue(serializer.is_valid())
        book = serializer.save()

        # Create BookCopies separately
        #for copy_data in book_copies_data:
        #    BookCopies.objects.create(book_id=book, **copy_data)

        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(BookCopies.objects.filter(book_id=book).count(), 10)

    def test_create_book_with_available_copies(self):
        book_data = self.create_book_data(
            'Test Book Available',
            random.choice(self.publishers),
            random.sample(self.authors, k=3),
            random.sample(self.categories, k=3),
            self.create_book_copies_data(1, ['Available'])
        )
        serializer = BookSerializer(data=book_data)
        self.assertTrue(serializer.is_valid())
        book = serializer.save()
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(BookCopies.objects.filter(book_id=book).count(), 1)

    def test_create_book_without_available_copies(self):
        book_data = self.create_book_data(
            'Test Book No Available',
            random.choice(self.publishers),
            random.sample(self.authors, k=3),
            random.sample(self.categories, k=3),
            []
        )
        serializer = BookSerializer(data=book_data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            self.fail("ValidationError was raised")
        self.assertTrue(serializer.is_valid())

    def test_create_multiple_books_with_copies(self):
        for i in range(51):
            book_data = self.create_book_data(
                f'Test Book {i}',
                random.choice(self.publishers),
                random.sample(self.authors, k=3),
                random.sample(self.categories, k=3),
                self.create_book_copies_data(100, [status[0] for status in BookCopies.BookStatus.choices])
            )
            serializer = BookSerializer(data=book_data)
            self.assertTrue(serializer.is_valid())
            serializer.save()
        self.assertEqual(Book.objects.count(), 51)
        for book in Book.objects.all():
            self.assertGreaterEqual(BookCopies.objects.filter(book_id=book).count(), 100)

    def test_quantity_of_available_copies(self):
        for i in range(51):
            book_data = self.create_book_data(
                f'Test Book {i}',
                random.choice(self.publishers),
                random.sample(self.authors, k=3),
                random.sample(self.categories, k=3),
                self.create_book_copies_data(100, [status[0] for status in BookCopies.BookStatus.choices])
            )
            serializer = BookSerializer(data=book_data)
            self.assertTrue(serializer.is_valid())
            serializer.save()
        for book in Book.objects.all():
            available_copies = BookCopies.objects.filter(book_id=book, status='Available').count()
            self.assertGreaterEqual(available_copies, 1)

    def test_create_multiple_books_with_different_status_copies(self):
        statuses = [status[0] for status in BookCopies.BookStatus.choices]
        for i in range(10):
            book_data = self.create_book_data(
                f'Test Book {i}',
                random.choice(self.publishers),
                random.sample(self.authors, k=3),
                random.sample(self.categories, k=3),
                [{'status': status} for status in statuses]
            )
            serializer = BookSerializer(data=book_data)
            self.assertTrue(serializer.is_valid())
            serializer.save()
        self.assertEqual(Book.objects.count(), 10)
        for book in Book.objects.all():
            self.assertEqual(BookCopies.objects.filter(book_id=book).count(), len(statuses))
            for status in statuses:
                self.assertEqual(BookCopies.objects.filter(book_id=book, status=status).count(), 1)

    def test_create_ten_books_with_hundred_available_copies(self):
        for i in range(10):
            book_data = self.create_book_data(
                f'Test Book {i}',
                random.choice(self.publishers),
                random.sample(self.authors, k=3),
                random.sample(self.categories, k=3),
                self.create_book_copies_data(100, ['Available'])
            )
            serializer = BookSerializer(data=book_data)
            self.assertTrue(serializer.is_valid())
            serializer.save()

        self.assertEqual(Book.objects.count(), 10)
        for book in Book.objects.all():
            self.assertEqual(BookCopies.objects.filter(book_id=book, status='Available').count(), 100)

        # Update 25% of the copies of each book to various other statuses
        statuses = [status[0] for status in BookCopies.BookStatus.choices if status[0] != 'Available']
        for book in Book.objects.all():
            copies_to_update = BookCopies.objects.filter(book_id=book)[:25]
            for copy in copies_to_update:
                new_status = random.choice(statuses)
                copy.status = new_status
                copy.save()

        # Verify the quantity of each status
        for book in Book.objects.all():
            #print(book.title)
            available_copies = BookCopies.objects.filter(book_id=book, status='Available').count()
            self.assertEqual(available_copies, 75)
            for status in statuses:
                #print(BookCopies.objects.filter(book_id=book, status=status).count(), "-", status)
                self.assertGreaterEqual(BookCopies.objects.filter(book_id=book, status=status).count(), 1)