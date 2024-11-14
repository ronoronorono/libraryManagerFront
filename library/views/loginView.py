from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from library.forms import loginForm

def loginView(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)
            if user is not None:
                print("NIGGERS")
                login(request, user)
                return redirect('/')
            
            else:
                print("NOT NIGGERS")
                form.add_error(None, "INVALIDO")
    else:
        form = loginForm()

    return render(request, 'both/login.html', {'form': form})