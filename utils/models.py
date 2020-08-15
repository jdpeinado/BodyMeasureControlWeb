"""Django models utilities."""

# Django
from django.db import models


class BMCModel(models.Model):
    """BodyMeasureControl base model.
    BMCModel acts as an abstract base class from which every
    other model in the project will inherit. This class provides
    every table with the following attributes:
        + created (DateTime): Store the datetime the object was created.
        + updated (DateTime): Store the last datetime the object was updated.
    """

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time on which the object was created.'
    )
    updated = models.DateTimeField(
        'updated at',
        auto_now=True,
        help_text='Date time on which the object was last updated.'
    )

    class Meta:
        """Meta option."""

        abstract = True

        get_latest_by = 'created'
        ordering = ['-created', '-updated']
