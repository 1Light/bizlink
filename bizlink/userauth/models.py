from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from django.db.models.signals import post_save

from django.core.validators import RegexValidator

# Creating a user option
USER_TYPE_CHOICES = (
        ('business_owner', 'Business Owner'),
        ('customer', 'Customer'),
)

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, username, first_name, last_name, password, mobile, address, user_type, **extra_fields):
        if not email:
            print("Email is not provided")
        
        if not password:
            print("Password is not provided")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            mobile = mobile,
            address = address,
            user_type = user_type,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self.db)

        return user
    
    def create_user(self, email, username, first_name, last_name, password, mobile, address, user_type, **extra_fields):
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, username, first_name, last_name, password, mobile, address, user_type, **extra_fields)
    
    def create_superuser(self, email, username, first_name, last_name, password, mobile="not_required", address="not_required", user_type="admin", **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self._create_user(email, username, first_name, last_name, password, mobile, address, user_type, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(db_index=True, unique=True, max_length=255)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.TextField(blank=False, null=False, default="This is my address")

    phone_regex = RegexValidator(regex=r'^\+?\d{9,15}$', message="Please input a valid phone number.")
    mobile = models.CharField(validators=[phone_regex], max_length=255)

    # Explicitly defining the built in password field (By AbstractBaseUser)
    password = models.CharField(max_length=128)

    # Extra Fields
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='business_owner')

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
    
    def __str__(self):
        return self.username

class BusinessOwner(CustomUser):

    class Meta:
        verbose_name = "Business Owner"
        verbose_name_plural = "Business Owners"

class Customer(CustomUser):
    pass

# Custom file upload path for user profile images
def profile_directory_path(instance, filename):
    return 'user_{0}/profile_images/{1}'.format(
        instance.created_by.id, filename
    )

class Profile(models.Model):
    created_by = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user_profile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_directory_path', blank=True, null=True, default="profile.jpg")
    full_name = models.CharField(max_length=250, blank=True, null=True, default="John Adams")
    bio = models.CharField(max_length=250, blank=True, null=True, default="I am awesome")
    mobile = models.CharField(max_length=250, blank=True, null=True, default="0987094994")
    verified = models.BooleanField(default=False)

    class Meta:
        ordering = ('full_name',)
        unique_together = ('created_by', 'mobile')
    
    def __str__(self):
        return self.full_name if self.full_name else self.created_by.username
    
    def profile_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' %(self.image.url))
    
class SocialMedia(models.Model):
    # Defining constants for platform choices
    FACEBOOK = 'facebook'
    TWITTER = 'twitter'
    INSTAGRAM = 'instagram'
    LINKEDIN = 'linkedin'
    YOUTUBE = 'youtube'
    TELEGRAM = 'telegram'

    # Choices for social media platforms
    PLATFORM_CHOICES = [
        (FACEBOOK, 'Facebook'),
        (TWITTER, 'Twitter'),
        (INSTAGRAM, 'Instagram'),
        (LINKEDIN, 'LinkedIn'),
        (YOUTUBE, 'YouTube'),
    ]

    # Field for selecting the platform
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    
    # URL field for the social media link
    url = models.URLField(max_length=200, blank=False)
    
    # Optional timestamp for when the link was created/modified
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_social_media', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Social Media"
        unique_together = ('created_by', 'url')

    def __str__(self):
        return f"{self.get_platform_display()} - {self.url}"

class Notification(models.Model):
    notificationId = ShortUUIDField(length=10, max_length=25, prefix="notification", alphabet="ABCDEF0123456789")

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Notifications"
    
    def __str__(self):
        return f"{self.message} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

