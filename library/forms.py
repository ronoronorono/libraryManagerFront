from django import forms

class loginForm(forms.Form):
    email = forms.EmailField(
        label="E-mail:",
        widget=forms.EmailInput(attrs={'placeholder': 'Digite seu e-mail'}),
        max_length=100
    )
    password = forms.CharField(
        label="Senha:",
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha'})
    )

class bookForm(forms.Form):
   title = forms.CharField(
        label="Título",
        max_length=100
   )
   subtitle = forms.CharField(
        label="Subtítulo",
        max_length=100
   )
   author = forms.CharField(
        label="Autor",
        max_length=100
   )
   ISBN = forms.CharField(
        label="ISBN",
        min_length=13,
        max_length=13
   )
   theme = forms.CharField(
        label="Gênero",
        max_length=100
   )

class studentForm(forms.Form):
   name = forms.CharField(
        label="Nome",
        max_length=100
   )
   RG = forms.CharField(
        label="RG",
        min_length=9,
        max_length=9
   )
   RA = forms.CharField(
        label="Matrícula",
        min_length=6,
        max_length=6
   )
   birthday = forms.DateField(
        label="Data de Nascimento",
         widget=forms.DateInput(format="%d-%m-%Y", attrs={"type": "date"}),
        input_formats=["%d-%m-%Y"]

   )