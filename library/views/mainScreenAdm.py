from django.shortcuts import render, redirect

def mainScreenAdmView(request):
    return render(request, 'adm/menuPrincipalAdm.html')