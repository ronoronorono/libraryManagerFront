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
