from django.contrib import admin
from .models.customUserProfile import *
from .models.author import *
# Register your models here.

class CustomUserProfileAdmin(admin.ModelAdmin):
    pass

class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUserProfile, CustomUserProfileAdmin)
admin.site.register(Author, AuthorAdmin)
