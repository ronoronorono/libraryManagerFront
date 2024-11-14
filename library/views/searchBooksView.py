from django.shortcuts import render, redirect

def searchBooksView(request):
    return render(request, 'both/buscarLivros.html')