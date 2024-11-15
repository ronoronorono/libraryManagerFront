from django.shortcuts import render, redirect
from library.forms import studentForm

def studentRegistrationView(request):
    if request.method == 'POST':
        form = studentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            RG = form.cleaned_data['RG']
            RA = form.cleaned_data['RA']
            birthday = form.cleaned_data['birthday']
            print(form.cleaned_data)
    else:
        form = studentForm() 

    return render(request, 'adm/cadastroDeAluno.html', {'studentForm': form})