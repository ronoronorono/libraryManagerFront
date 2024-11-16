from django.shortcuts import render, redirect
from library.forms import studentForm
from library.models import Student

from django.core.exceptions import ValidationError

def studentsAdminView(request):
    return render(request, 'adm/admAlunos.html')