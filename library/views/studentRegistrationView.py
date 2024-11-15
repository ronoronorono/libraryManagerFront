from django.shortcuts import render, redirect
from library.forms import studentForm
from library.models import Student

from django.core.exceptions import ValidationError

def studentRegistrationView(request):
    if request.method == 'POST':
        form = studentForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.save()
        else:
            print("deu ruim")
            return render(request, 'adm/cadastroDeAluno.html', {'studentForm': form})
    else:
        form = studentForm() 
        return render(request, 'adm/cadastroDeAluno.html', {'studentForm': form})
    
    return render(request, 'adm/cadastroDeAluno.html', {'studentForm': form})