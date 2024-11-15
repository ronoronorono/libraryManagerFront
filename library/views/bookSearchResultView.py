from django.shortcuts import render, redirect
from library.models.book import Book

def bookSearchResultView(request):
    title = request.GET.get('title', '')
    resultado = Book.objects.filter(title__contains=title)
    print(resultado)

    return render(request, 'both/resultadoBuscaLivro.html', {'resultado': resultado})