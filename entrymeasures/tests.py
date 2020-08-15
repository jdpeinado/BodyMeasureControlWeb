"""EntryMeasure tests."""

# Django
from django.test import TestCase

# Django REST framework
from rest_framework.authtoken.models import Token

# Test
from tests import GeneralTestCase

# Model
from users.models import User, Profile
from entrymeasures.models import EntryMeasure

# Utils
from measurement.measures import Weight, Distance
from django.utils import timezone
from datetime import timedelta


class EntryMeasureTestCase(GeneralTestCase):
    """EntryMeasure tests case."""

    def test_list_entrymeasures(self):
        """Test get entrymeasures for a user."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/entrymeasures/')
        assert response.status_code == 200
        assert response.data['count'] == EntryMeasure.objects.filter(user=self.user, active=True).count()

    def test_retrieve_entrymeasure(self):
        """Test entrymeasure by date is correct."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # right date_measure
        date = self.entrymeasure.date_measure
        response = self.client.get('/entrymeasures/{}/'.format(str(date.date())))
        assert response.status_code == 200
        assert response.data['id'] == self.entrymeasure.id

        # wrong date_measure
        response = self.client.get('/entrymeasures/2000-04-01/')
        assert response.status_code == 404
        assert response.data['detail'] == 'Not found.'

    def test_create_entrymeasure(self):
        """Test create entrymeasure."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # no passing arguments
        response = self.client.post('/entrymeasures/')
        assert response.status_code == 400

        # no passing bodyweight and date_measure today (there is already a today measure)
        data = {
            'chest': 102.,
            'waist': 89.,
            'hip': 90.2,
            'leg': 57.4,
            'bicep': 32.5
        }
        response = self.client.post('/entrymeasures/', data)
        assert response.status_code == 400
        assert response.data['bodyweight'][0] == 'This field is required.'
        assert response.data['date_measure'][0] == 'There is already a measure for the given today date'

        # right creaation
        data['bodyweight'] = 77.9
        data['date_measure'] = timezone.now().date() - timedelta(days=1)
        response = self.client.post('/entrymeasures/', data)
        assert response.status_code == 201
        assert EntryMeasure.objects.filter(user=self.user, active=True).count() == 2

    def test_delete_entrymeasure(self):
        """Test delete entrymeasure."""

        # it should not be deleted, just active=False
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        date = self.entrymeasure.date_measure
        response = self.client.delete('/entrymeasures/{}/'.format(str(date.date())))
        assert response.status_code == 204
        self.entrymeasure = EntryMeasure.objects.first()
        assert not self.entrymeasure.active
        self.entrymeasure.active = True
        self.entrymeasure.save()

    def test_update_entrymeasure(self):
        """Test update entrymeasure."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        date = self.entrymeasure.date_measure
        url = '/entrymeasures/{}/'.format(str(date.date()))

        # field required
        data = {
            'chest': 102.7,
            'waist': 87.3,
            'hip': 89,
            'leg': 57.7,
            'bicep': 32.6
        }
        response = self.client.put(url, data)
        assert response.status_code == 400
        assert response.data['bodyweight'][0] == 'This field is required.'

        # right update
        data = {
            'chest': 102.7,
            'waist': 87.3,
            'hip': 89,
            'leg': 57.7,
            'bicep': 32.6,
            'bodyweight': 80.1
        }
        response = self.client.put(url, data)
        assert response.status_code == 200
        assert round(EntryMeasure.objects.first().chest.cm, 2) == 102.7

    def test_partial_update(self):
        """Test partial update entrymeasure."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        date = self.entrymeasure.date_measure
        url = '/entrymeasures/{}/'.format(str(date.date()))

        # no fields
        response = self.client.patch(url)
        assert response.status_code == 200

        # partial update a field
        data = {
            'chest': 101
        }
        response = self.client.patch(url, data)
        assert response.status_code == 200
        assert round(EntryMeasure.objects.first().chest.cm, 2) == 101.0
