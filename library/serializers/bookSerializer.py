from rest_framework import serializers
from library.models import Book, BookCopies

class BookCopiesSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()

    class Meta:
        model = BookCopies
        fields = ('book_id', 'status','quantity')

    @staticmethod
    def get_quantity(obj):
        return obj.book_id.count()


class BookSerializer(serializers.ModelSerializer):
    book_copies = BookCopiesSerializer(many=True)
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'category', 'publisher', 'year', 'description', 'updated_at', 'is_active', 'deleted_at', 'book_copies')

    def validate_book_copies(self, value):
        if len(value) < 0:
            raise serializers.ValidationError('Book copies cannot be empty')
        return value

    def create(self, validated_data):
        book_copies_data = validated_data.pop('book_copies')
        author_data = validated_data.pop('author')
        category_data = validated_data.pop('category')


        book = Book.objects.create(**validated_data)
        for category in category_data:
            book.category.add(category)
            book.save()
        for author in author_data:
            book.author.add(author)
            book.save()
        for book_copy_data in book_copies_data:
            BookCopies.objects.create(book_id=book, **book_copy_data)
        return book
