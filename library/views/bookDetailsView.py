from django.shortcuts import render, redirect
from library.models.book import Book

def bookDetailsView(request):
    bookID = request.GET.get('livro', '')
    print("ID DO LIVRO: "+bookID)
    book = Book.objects.get(pk=bookID)
    print(book)

    return render(request, 'both/detalhesLivro.html', {'book': book})