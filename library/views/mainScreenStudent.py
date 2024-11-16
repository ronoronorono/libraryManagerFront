from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def mainScreenStudentView(request):
    return render(request, 'aluno/menuPrincipalAluno.html')