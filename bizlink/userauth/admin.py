from django.contrib import admin
from .models import CustomUser

# Class for Tabular Representation of User Details
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']

# Register your models here.
admin.site.register(CustomUser, UserAdmin)