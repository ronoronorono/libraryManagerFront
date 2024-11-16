"""
URL configuration for libraryManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from library.views.loginView import loginView
from library.views.mainScreenAdm import mainScreenAdmView
from library.views.mainScreenStudent import mainScreenStudentView
from library.views.bookRegistrationView import bookRegistrationView
from library.views.studentRegistrationView import studentRegistrationView
from library.views.searchBooksView import searchBooksView
from library.views.bookSearchResultView import bookSearchResultView
from library.views.bookDetailsView import bookDetailsView
from library.views.borrowedBooksView import borrowedBooksView
from library.views.studentsAdminView import studentsAdminView

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path('api/v1/', include('library.urls')),
    path('api/auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('login/', loginView, name='login'),
    path('menuAdm/', mainScreenAdmView, name='menuAdm'),
    path('menuAluno/', mainScreenStudentView, name='menuAluno'),
    path('cadastroLivro/', bookRegistrationView, name='cadastroLivro'),
    path('cadastroAluno/', studentRegistrationView, name='cadastroAluno'),
    path('buscarLivros/', searchBooksView, name='buscarLivros'),
    path('resultadoBuscaLivro/', bookSearchResultView, name='resultadoBuscaLivro'),
    path('detalhesLivro/', bookDetailsView, name='detalhesLivro'),
    path('emprestimos/', borrowedBooksView, name='emprestimos'),
    path('admAlunos/', studentsAdminView, name='admAlunos'),
]
