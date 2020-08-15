"""Users models"""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser

# Models
from django_measurement.models import MeasurementField
from cloudinary.models import CloudinaryField

# Utils
from measurement.measures import Distance
from utils.models import BMCModel


class User(BMCModel, AbstractUser):
    """User model.
    Extend from Django's Abstract User, change the username field
    to email and add some extra fields.
    """

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    is_verified = models.BooleanField(
        'verified',
        default=True,
        help_text='Set to true when the user have verified its email address.'
    )

    def __str__(self):
        """Return username."""
        return self.username

    def get_short_name(self):
        """Return username."""
        return self.username


class Profile(models.Model):
    """Profile model.

    Proxy model that extends the base data with other
    information.
    """

    class UnitMeasurement(models.TextChoices):
        """
        Class to deal with enum unit measures
        Two posibles values: 0: METRIC, 1:IMPERIAL
        """

        METRIC = "METRIC"
        IMPERIAL = "IMPERIAL"

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)

    picture = CloudinaryField(
        "Profile user picture",
        blank=True,
        null=True
    )

    height = MeasurementField(
        measurement=Distance,
        unit_choices=(('ft', 'ft'), ('m', 'm')),
        blank=True,
        null=True
    )
    measurement_system = models.CharField(
        blank=True,
        choices=[(tag, tag.value) for tag in UnitMeasurement],
        default=UnitMeasurement.METRIC,
        max_length=8
    )
    country_code = models.CharField(blank=True, max_length=2)

    active = models.BooleanField(default=True)

    def __str__(self):
        """Return username."""
        return self.user.username
