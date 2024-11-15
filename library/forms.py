from django import forms
from library.models import Student

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


class studentForm(forms.ModelForm):
     RA = forms.CharField(
        label="Numero Matrícula",
        min_length=6,
        max_length=6
     )
     RG = forms.CharField(
        label="RG",
        min_length=9,
        max_length=9
     )
     class Meta:
          model = Student
          fields = ["RA", "RG", "name", "birthday"]
          labels = {
               "name":"Nome",
               "birthday":"Data de Nascimento"
          }
          widgets = {
               "birthday" : forms.DateInput(format="%d/%m/%Y", attrs={"type": "date"}),
               }

     def clean(self):
          super(studentForm, self).clean()

          RA = self.cleaned_data.get('RA')
          RG = self.cleaned_data.get('RG')
          if Student.objects.filter(RG=RG).exists():
               self._errors['RG'] = self.error_class([
                   'RG Existente'])

          if Student.objects.filter(RA=RA).exists():
               self._errors['RA'] = self.error_class([
                   'RA Existente'])

          return self.cleaned_data
          

class searchBookForm(forms.Form):
     title = forms.CharField(
        label="Título",
        max_length=100
     )

