from django.contrib import admin
from .models.book import *
from .models.student import *
# Register your models here.

#class AuthorAdmin(admin.ModelAdmin):
    #pass

#admin.site.register(Author, AuthorAdmin)
admin.site.register(Book)
admin.site.register(Student)