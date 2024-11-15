from django.shortcuts import render, redirect
from library.forms import searchBookForm
from library.models.book import Book

def searchBooksView(request):
    if request.method == 'POST':
        form = searchBookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            print(form.cleaned_data)
            resultado=Book.objects.filter(title__contains=title)
            print(resultado)
       
    else:
        form = searchBookForm() 
    return render(request, 'both/buscarLivros.html', {'searchBookForm': form})