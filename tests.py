"""Class to define all the data is going to be used in testing every app."""

# Django
from django.test import TestCase

# Django REST framework
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Model
from users.models import User, Profile
from entrymeasures.models import EntryMeasure

# Utils
from measurement.measures import Weight, Distance


class GeneralTestCase(APITestCase):
    """General tests case."""

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create_user(
            first_name='Fake first name',
            last_name='Fake last name',
            email='fake_email@email.com',
            username='fakeusername',
            password='Admin12345'
        )
        self.profile = Profile.objects.create(
            user=self.user
        )
        self.token = Token.objects.create(user=self.user)

        self.user2 = User.objects.create_user(
            first_name='Fake first name',
            last_name='Fake last name',
            email='fake_email2@email.com',
            username='fakeusername2',
            password='Admin12345'
        )
        self.profile2 = Profile.objects.create(
            user=self.user2
        )
        self.token2 = Token.objects.create(user=self.user2)

        self.entrymeasure = EntryMeasure.objects.create(
            user=self.user,
            profile=self.profile,
            chest=Distance(cm=102),
            waist=Distance(cm=89.5),
            hip=Distance(cm=1090.12),
            leg=Distance(cm=57),
            bicep=Distance(cm=32.5),
            bodyweight=Weight(kg=78.4)
        )
