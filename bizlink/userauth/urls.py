from django.urls import path
from . import views

app_name = "userauth"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("user_login/", views.user_login, name="user_login"),
    path("user_logout/", views.user_logout, name="user_logout"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path('manage_social_media/', views.manage_social_media, name='manage_social_media'),
]