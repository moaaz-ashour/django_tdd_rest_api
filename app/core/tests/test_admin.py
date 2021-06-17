from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        """Create a super user and log him in
           Create a user"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = "admin@example.com",
            password = "admin"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = "user@example.com",
            password = "testuser",
            name="test user"
        )
    
    def test_user_listed(self):
        """Test that users are listed in user page
        """
        # Generate url for users list page
        # These urls are listed in django admin docs
        # Gets the URL that lists users in admin page
        # PS: Have to register User model to admin for this url to work
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        # AssertContains checks if certain value is present in a dict
        # Also checks if the http respose is OK (200)
        # name field is not available in default UserAdmin class
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)