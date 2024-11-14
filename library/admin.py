from django.contrib import admin
from .models.author import *
# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Author, AuthorAdmin)
