from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def borrowedBooksView(request):
    return render(request, 'aluno/emprestimos.html')