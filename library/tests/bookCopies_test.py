# library/tests/bookCopies_test.py

from django.test import TestCase
from library.models.book import Book
from library.models.author import Author
from library.models.categories import Category
from library.models.publisher import Publisher
from library.models.book_copies import BookCopies
import random

class BookCopiesTest(TestCase):

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

        # Create 30 books
        self.books = []
        for i in range(30):
            book = Book.objects.create(
                title=f'Book{i}',
                publisher=random.choice(self.publishers),
                year=2023,
                description=f'Description of Book{i}'
            )
            book.author.set(random.sample(self.authors, k=random.randint(1, 3)))
            book.category.set(random.sample(self.categories, k=random.randint(1, 3)))
            self.books.append(book)

        # Create up to 30 copies for each book with random statuses
        self.book_copies = []
        statuses = BookCopies.BookStatus.choices
        for book in self.books:
            num_copies = random.randint(1, 30)
            for _ in range(num_copies):
                status = random.choice(statuses)[0]
                book_copy = BookCopies.objects.create(book_id=book, status=status)
                self.book_copies.append(book_copy)

    def test_books_and_copies(self):
        self.assertEqual(len(self.books), 30)
        for book in self.books:
            self.assertGreaterEqual(book.book.count(), 1)
            self.assertLessEqual(book.book.count(), 30)