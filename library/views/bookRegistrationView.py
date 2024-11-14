from django.shortcuts import render, redirect
from library.forms import bookForm
from library.models import Book

def bookRegistrationView(request):
    if request.method == 'POST':
        form = bookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            subtitle = form.cleaned_data['subtitle']
            author = form.cleaned_data['author']
            ISBN = form.cleaned_data['ISBN']
            theme = form.cleaned_data['theme']
            print(form.cleaned_data)
            book = Book.objects.create(id=ISBN, title=title, subtitle=subtitle, author=author, theme=theme)
       
    else:
        form = bookForm() 
    return render(request, 'adm/cadastroDeLivro.html', {'bookForm': form})