from django.shortcuts import render, redirect

def bookSearchResultView(request):
    return render(request, 'both/resultadoBuscaLivro.html')