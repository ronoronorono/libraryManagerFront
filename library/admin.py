from django.contrib import admin
from .models.customUserProfile import *
# Register your models here.

class CustomUserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUserProfile, CustomUserProfileAdmin)

