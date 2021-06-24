from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")


def create_user(**params):
    """
        helper function to create test users
    """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """
        Test the users API (public)
       'Public' because we dont check for authentication
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """
            test API call to create user with valid payload
            payload is a POST dict
        """

        payload = {
            'email': 'test@test.com',
            'password': 'testpass',
            'name': 'tester'
        }

        # Make a request: this call to API should create a new user
        res = self.client.post(CREATE_USER_URL, payload)

        # assert if the response is 201 created
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # get this user and check if password is correct
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        # assert that the password is not returned in the response data
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """
            Test API when trying to create existing users
        """
        # Note: the users created in previous test cases do not exist
        payload = {
            'email': 'test@test.com',
            'password': 'testpass',
            'name': 'test'
        }
        # create this test user
        create_user(**payload)

        # make a request and try to create this user again with APIClient
        res = self.client.post(CREATE_USER_URL, payload)
        # assert that the response is 400
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
            Test if user is not created when password is too short
        """
        # Note, the users created in previous test cases do not exist
        payload = {
            'email': 'test@test.com',
            'password': 'tp',
            'name': 'test'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        # assert response failed
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # assert user was not created
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """
            test if token can be created successfully \
            with valid creds for existing user
        """
        payload = {
            'email': 'test@test.com',
            'password': 'testpass',
            'name': 'tester'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        # we should get a HTTP 200 response and
        # it should contain a token in the data response
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def create_token_invalid_credentials(self):
        """
            test that token is not created created
            if invalid credentials were given
        """
        create_user(
            email='test@test.com',
            password='testpass'
        )

        payload = {
            'email': 'test@test.com',
            'password': 'wrongpass'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def create_token_no_user(self):
        """
            test if token cannot be created
            if user doesn't exist
        """
        payload = {
            'email': 'test@test.com',
            'password': 'testpass'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def create_token_missing_field(self):
        """
            test if token is not created when a fied is left blank
        """
        payload = {
            'email': 'test@test.com',
            'password': 'testpass'
        }
        create_user(**payload)
        payload = {
            'email': 'test@test.com',
            'password': ''
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
