"""Users tests."""

# Django
from django.test import TestCase

# Django REST framework
from rest_framework.authtoken.models import Token

# Test
from tests import GeneralTestCase

# Model
from users.models import User, Profile

# Utils
from measurement.measures import Distance


class UserTestCase(GeneralTestCase):
    """User tests case."""

    def test_signup(self):
        """Test correct signup."""
        url = '/users/signup/'

        # signup a user correctly
        data = {
            "username": "test",
            "password": "Admin12345",
            "password_confirmation": "Admin12345",
            "email": "test@email.com"
        }
        response = self.client.post(url, data)
        assert response.status_code == 201
        assert User.objects.filter(email='test@email.com').count() == 1
        assert User.objects.filter(username='test').count() == 1
        assert Profile.objects.filter(user__email='test@email.com').count() == 1

        # try to signup the same user
        response = self.client.post(url, data)
        assert response.status_code == 400
        assert response.data['username'][0] == 'This field must be unique.'
        assert response.data['email'][0] == 'This field must be unique.'

        # signup passwords don't match
        data = {
            "username": "test1",
            "password": "Admin12345",
            "password_confirmation": "Admin12346",
            "email": "test1@email.com"
        }
        response = self.client.post(url, data)
        assert response.status_code == 400
        assert response.data['non_field_errors'][0] == "Passwords don't match"

    def test_login(self):
        """Test correct login."""
        url = '/users/login/'

        # right login
        data = {
            'email': self.user.email,
            'password': 'Admin12345'
        }
        response = self.client.post(url, data)
        assert response.status_code == 201

        # user not verified
        self.user.is_verified = False
        self.user.save()
        response = self.client.post(url, data)
        assert response.status_code == 400
        assert response.data['non_field_errors'][0] == 'Account is not active yet :('
        self.user.is_verified = False
        self.user.save()

        # invalid credentials
        data = {
            'email': 'bad@email.com',
            'password': 'bad_password'
        }
        response = self.client.post(url, data)
        assert response.status_code == 400
        assert response.data['non_field_errors'][0] == 'Invalid credentials'

        # invalid fields
        data = {
            'email': 'bad',
            'password': 'bad'
        }
        response = self.client.post(url, data)
        assert response.status_code == 400
        assert response.data['email'][0] == 'Enter a valid email address.'
        assert response.data['password'][0] == 'Ensure this field has at least 8 characters.'

    def test_retrieve(self):
        """Test retrieve."""
        url = '/users/fakeusername/'

        # without authorization token
        response = self.client.get(url)
        assert response.status_code == 401
        assert response.data['detail'] == 'Authentication credentials were not provided.'

        # wrong token (wrong user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.get(url)
        assert response.status_code == 403
        assert response.data['detail'] == 'You do not have permission to perform this action.'

        # invalid token
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid_token')
        response = self.client.get(url)
        assert response.status_code == 401
        assert response.data['detail'] == 'Invalid token.'

        # right retrieve
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)
        assert response.status_code == 200

    def test_update_user(self):
        """Test update user."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put(
            '/users/fakeusername/',
            data={
                'first_name': 'Jon',
                'last_name': 'López'
            }
        )
        assert response.status_code == 200
        user_updated = User.objects.get(email=self.user.email)
        assert user_updated.first_name == 'Jon'
        assert user_updated.last_name == 'López'

    def test_partial_update_user(self):
        """Test partial update user."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.patch(
            '/users/fakeusername/',
            data={
                'first_name': 'Ángel',
            }
        )
        assert response.status_code == 200
        user_updated = User.objects.get(email=self.user.email)
        assert user_updated.first_name == 'Ángel'

    def test_update_profile(self):
        """Test update profile."""
        url = '/users/fakeusername/profile/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # right update
        data = {
            'measurement_system': 'METRIC',
            'height': 1.84,
            'country_code': 'ES'
        }
        response = self.client.put(url, data)
        assert response.status_code == 200
        profile_updated = Profile.objects.get(user=self.user)
        assert profile_updated.country_code == 'ES'
        assert profile_updated.height.m == 1.84
        assert profile_updated.measurement_system == 'METRIC'

        # bad fields update
        data = {
            'measurement_system': 'METRICfff',
            'country_code': 'ESff'
        }
        response = self.client.put(url, data)
        assert response.status_code == 400
        assert response.data['measurement_system'][0] == '"METRICfff" is not a valid choice.'
        assert response.data['country_code'][0] == 'Ensure this field has no more than 2 characters.'

        # change to imperial system
        data = {
            'measurement_system': 'IMPERIAL'
        }
        response = self.client.put(url, data)
        assert response.status_code == 200
        profile_updated = Profile.objects.get(user=self.user)
        assert profile_updated.measurement_system == 'IMPERIAL'
        assert round(profile_updated.height.ft, 2) == response.data['profile']['height']
