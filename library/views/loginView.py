from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from library.forms import loginForm
from django.contrib.auth.models import User

#user = User.objects.create_user("TESTE", "TESTE@TESTE.com", "TESTE123")
#user.save()

def loginView(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']


            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                print("LOGADO")
                login(request, user)
                return redirect('menuAdm/')
            
            else:
                print("NOT LOGADO")
                form.add_error(None, "INVALIDO")
    else:
        form = loginForm()

    return render(request, 'both/login.html', {'form': form})