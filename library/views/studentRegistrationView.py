from django.shortcuts import render, redirect
from library.forms import studentForm
from library.models import Student

def studentRegistrationView(request):
    if request.method == 'POST':
        form = studentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            RG = form.cleaned_data['RG']
            RA = form.cleaned_data['RA']
            birthday = form.cleaned_data['birthday']
            print(form.cleaned_data)
            student = Student.objects.create(RG=RG, RA=RA, name=name, birthday=birthday)
        else:
            print("deu ruim")
            print(form.errors)
    else:
        form = studentForm() 

    return render(request, 'adm/cadastroDeAluno.html', {'studentForm': form})