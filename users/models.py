"""Users models"""

# Django
from django.db import models
from django.contrib.auth.models import User

# Models
from django_measurement.models import MeasurementField
from cloudinary.models import CloudinaryField

# Utils
from measurement.measures import Distance


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

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    picture = CloudinaryField(
        "Profile user picture",
        blank=True,
        null=True
    )

    height = MeasurementField(measurement=Distance, unit_choices=(('ft', 'ft'), ('m', 'm')), blank=True, null=True)
    measurement_system = models.CharField(
        blank=True,
        choices=[(tag, tag.value) for tag in UnitMeasurement],
        default=UnitMeasurement.METRIC,
        max_length=8
    )
    country_code = models.CharField(blank=True,max_length=2)
    
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return username."""
        return self.user.username