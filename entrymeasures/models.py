"""EntryMeasures models """

# Django
from django.db import models
from django.contrib.auth.models import User

# Models
from users.models import Profile

# Utils
from datetime import datetime

class EntryMeasure(models.Model):
    """
    Entry measurement class to store every measure of the user by day
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_measure = models.DateField(auto_now_add=True,unique=True)
    
    front_image_url = models.ImageField(
        upload_to='entrymeasures/pictures',
        blank=True,
        null=True
    )
    side_image_url = models.ImageField(
        upload_to='entrymeasures/pictures',
        blank=True,
        null=True
    )
    back_image_url = models.ImageField(
        upload_to='entrymeasures/pictures',
        blank=True,
        null=True
    )

    chest = models.DecimalField(max_digits=5,decimal_places=2)
    waist = models.DecimalField(max_digits=5,decimal_places=2)
    hip = models.DecimalField(max_digits=5,decimal_places=2)
    leg = models.DecimalField(max_digits=5,decimal_places=2)
    bicep = models.DecimalField(max_digits=5,decimal_places=2)
    bodyweight = models.DecimalField(max_digits=5,decimal_places=2)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return user and date of the measure"""
        return "{} measure for {}".format(self.user.username, self.date_measure)
