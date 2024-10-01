from django.contrib import admin
from .models import CustomUser, Profile, SocialMedia, Notification

# Class for Tabular Representation of User Details
class SocialMediaAdmin(admin.TabularInline):
    model = SocialMedia
    extra = 1 
    list_display = ['platform', 'url']

class NotificationAdmin(admin.TabularInline):
    model = Notification
    list_display = ['created_by', 'message', 'created_at']  # Specify fields to display
    readonly_fields = ['created_at']  # Make created_at read-only
    extra = 1  # Number of empty forms to display

class UserAdmin(admin.ModelAdmin):
    inlines = [SocialMediaAdmin, NotificationAdmin]
    list_display = ['username', 'email']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'full_name', 'profile_image', 'mobile', 'verified']

# Register your models here.
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Profile, ProfileAdmin)