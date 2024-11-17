from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from library.forms import loginForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.http import HttpResponse

#user = User.objects.create_user("TESTE", "TESTE@TESTE.com", "TESTE123")
#user.save()

def loginView(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']


            user = authenticate(request, username=email, password=password)
            #permissions = Permission.objects.filter(user=request.user)
            auth_user = User.objects.get(username=email)
            print("SUPERUSER: "+str(User.objects.get(username=email).is_superuser))
            response = HttpResponse('COOKAO')
            
            if user is not None:
                if auth_user.is_superuser:
                    print("LOGADO ADM")
                    request.session.setdefault('student', False)
                    login(request, user)
                    return redirect('/menuAdm')
                else:
                    print("LOGADO ALUNO")
                    request.session.setdefault('student', True)
                    login(request, user)
                    return redirect('/menuAluno')
            
            else:
                print("NOT LOGADO")
                form.add_error(None, "INVALIDO")
    else:
        form = loginForm()

    return render(request, 'both/login.html', {'form': form})