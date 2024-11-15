from django.shortcuts import render, redirect
from library.forms import searchBookForm

def searchBooksView(request):
    if request.method == 'POST':
        form = searchBookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            return redirect(f'/resultadoBuscaLivro?title={title}')
       
    else:
        form = searchBookForm() 

    return render(request, 'both/buscarLivros.html', {'searchBookForm': form})