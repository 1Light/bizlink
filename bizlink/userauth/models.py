from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

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
    address = models.CharField(max_length=255)

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