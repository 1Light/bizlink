from django import forms
from .models import CustomUser, USER_TYPE_CHOICES
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

INPUT_CLASSES = 'input-box form-control'

class SignUpForm(UserCreationForm):
    usable_password = None

    password1 = forms.CharField(
        label = 'Password',
        widget = forms.PasswordInput(attrs={
            'class': INPUT_CLASSES
        })
    )

    password2 = forms.CharField(
        label = 'Confirm Password',
        widget = forms.PasswordInput(attrs={
            'class': INPUT_CLASSES
        })
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username', 'mobile', 'address', 'password1', 'password2', 'user_type')

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'last_name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'email': forms.EmailInput(attrs={
                'class': INPUT_CLASSES
            }),
            'username': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'mobile': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'address':  forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'password1': forms.PasswordInput(attrs={
                'class': INPUT_CLASSES
            }),
            'password2': forms.PasswordInput(attrs={
                'class': INPUT_CLASSES
            }),
            'user_type': forms.Select(choices=USER_TYPE_CHOICES, attrs={
                'class': INPUT_CLASSES
            }),
        }

        labels = {
            'first_name':'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'username': 'Username',
            'mobile': 'Mobile',
            'address': 'Address',
            'password1': 'Password',
            'password2': 'Confirm Password',
            'user_type': 'User Type',
        }
    
"""     def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user_type = self.cleaned_data.get('user_type')

        if user_type == 'business_owner':
            user.shop_name = self.cleaned_data.get('shop_name')
        else:
            user.shop_name = None

        if commit:
            user.save()
        return user """

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        "invalid_login": _("Invalid username or password. Please try again."),
        "inactive": _("This account is inactive."),
        "no_user": _("User does not exist")
    }

    def clean(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if email is not None and password:

            UserModel = get_user_model()
            email = email.strip().lower()

            try:
                # Check if the user exists
                self.user = UserModel.objects.get(email=email)
                if not self.user.check_password(password):
                    raise self.get_invalid_login_error()
            except UserModel.DoesNotExist:
                # User does not exist, raise invalid login error
                raise self.get_user_does_not_exist()
            
            # If user exists, check if they are active
            if not self.user.is_active:
                # User is inactive, raise a custom validation error
                raise self.confirm_login_allowed(self.user)

        return self.cleaned_data
    
    def get_user_does_not_exist(self):
        return ValidationError(
            self.error_messages["no_user"],
            code="no_user"
        )

class LogInForm(CustomAuthenticationForm):

    username = forms.EmailField(
        label = 'Email',
        widget = forms.EmailInput(attrs={
            'class': INPUT_CLASSES
        })
    )

    password = forms.CharField(
        label = 'Password',
        widget = forms.PasswordInput(attrs={
            'class': INPUT_CLASSES
        })
    )

    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        label='User Type',
        widget=forms.Select(attrs={
            'class': INPUT_CLASSES
        }),
    )