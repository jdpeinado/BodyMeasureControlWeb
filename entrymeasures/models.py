"""EntryMeasures models """

# Django
from django.db import models
from django.db.models.signals import pre_delete

# Models
from users.models import Profile, User
from django_measurement.models import MeasurementField
from cloudinary.models import CloudinaryField

# Utils
from django.utils import timezone
from measurement.measures import Weight, Distance
import cloudinary


class EntryMeasure(models.Model):
    """
    Entry measurement class to store every measure of the user by day
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_measure = models.DateField(default=timezone.now)

    front_image_url = CloudinaryField(
        "Front image",
        blank=True,
        null=True
    )
    side_image_url = CloudinaryField(
        "Side image",
        blank=True,
        null=True
    )
    back_image_url = CloudinaryField(
        "Back image",
        blank=True,
        null=True
    )

    chest = MeasurementField(
        measurement=Distance,
        unit_choices=(('inch', 'in'), ('cm', 'cm'))
    )
    waist = MeasurementField(
        measurement=Distance,
        unit_choices=(('inch', 'in'), ('cm', 'cm'))
    )
    hip = MeasurementField(
        measurement=Distance,
        unit_choices=(('inch', 'in'), ('cm', 'cm'))
    )
    leg = MeasurementField(
        measurement=Distance,
        unit_choices=(('inch', 'in'), ('cm', 'cm'))
    )
    bicep = MeasurementField(
        measurement=Distance,
        unit_choices=(('inch', 'in'), ('cm', 'cm'))
    )
    bodyweight = MeasurementField(
        measurement=Weight,
        unit_choices=(('lb', 'lb'), ('kg', 'kg'))
    )

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'date_measure',)

    def __str__(self):
        """Return user and date of the measure"""
        return "{} measure for {}".format(
            self.user.username, self.date_measure)

    def change_units(self, measurement_system):
        """Change unit to new one"""

        if measurement_system == 'METRIC':
            self.bodyweight = Weight(kg=self.bodyweight.kg)
            self.chest = Distance(cm=self.chest.cm)
            self.waist = Distance(cm=self.waist.cm)
            self.hip = Distance(cm=self.hip.cm)
            self.leg = Distance(cm=self.leg.cm)
            self.bicep = Distance(cm=self.bicep.cm)
        else:
            self.bodyweight = Weight(lb=self.bodyweight.lb)
            self.chest = Distance(inch=self.chest.inch)
            self.waist = Distance(inch=self.waist.inch)
            self.hip = Distance(inch=self.hip.inch)
            self.leg = Distance(inch=self.leg.inch)
            self.bicep = Distance(inch=self.bicep.inch)


def remove_images_from_cloud(sender, instance, **kwargs):
    entrymeasure = instance
    if entrymeasure.front_image_url:
        cloudinary.uploader.destroy(
            entrymeasure.front_image_url.public_id,
            invalidate=True
        )
    if entrymeasure.side_image_url:
        cloudinary.uploader.destroy(
            entrymeasure.side_image_url.public_id,
            invalidate=True
        )
    if entrymeasure.back_image_url:
        cloudinary.uploader.destroy(
            entrymeasure.back_image_url.public_id,
            invalidate=True
        )


pre_delete.connect(remove_images_from_cloud, sender=EntryMeasure)
