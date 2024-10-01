from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Profile

class ProfileTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret",
            first_name="Test",
            last_name="User",
            mobile="1234567890",  # Ensure you include all required fields
            address="123 Test St",  # Include necessary fields as per your model
            user_type="customer"  # Specify user type
        )

    def test_profile_created(self):
        # Check that a Profile is created for the user
        profile = Profile.objects.get(created_by=self.user)
        self.assertEqual(profile.created_by, self.user)  # This checks that the profile's created_by is the user
