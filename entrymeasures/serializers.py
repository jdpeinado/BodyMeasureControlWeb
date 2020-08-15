"""EntryMeasures Serializers."""

# Model
from entrymeasures.models import EntryMeasure  # noqa: F401

# Django REST framework
from rest_framework import serializers

# Utils
from measurement.measures import Weight, Distance
from django.utils import timezone
import cloudinary


class EntryMeasureModelSerializer(serializers.ModelSerializer):
    """EntryMeasure model serializer."""

    class Meta:
        """Meta class."""

        model = EntryMeasure
        fields = (
            'id',
            'date_measure',
            'chest',
            'waist',
            'hip',
            'leg',
            'bicep',
            'bodyweight',
            'front_image_url',
            'side_image_url',
            'back_image_url',
        )
        read_only_fields = (
            'id',
            'date_measure',
        )

    def to_representation(self, instance):
        """

        Transform measurement objects to decimal values for validating.
        Transform cloudinary objects to char values for validating.
        """
        profile = self.context['request'].user.profile
        if instance.front_image_url:
            instance.front_image_url = instance.front_image_url.url

        if instance.side_image_url:
            instance.side_image_url = instance.side_image_url.url

        if instance.back_image_url:
            instance.back_image_url = instance.back_image_url.url

        if profile.measurement_system == 'METRIC':
            instance.chest = round(instance.chest.cm, 2)
            instance.waist = round(instance.waist.cm, 2)
            instance.hip = round(instance.hip.cm, 2)
            instance.leg = round(instance.leg.cm, 2)
            instance.bicep = round(instance.bicep.cm, 2)
            instance.bodyweight = round(instance.bodyweight.kg, 2)
        else:
            instance.chest = round(instance.chest.inch, 2)
            instance.waist = round(instance.waist.inch, 2)
            instance.hip = round(instance.hip.inch, 2)
            instance.leg = round(instance.leg.inch, 2)
            instance.bicep = round(instance.bicep.inch, 2)
            instance.bodyweight = round(instance.bodyweight.lb, 2)
        ret = super().to_representation(instance)

        return ret

    def update(self, instance, data):
        """Update data"""

        profile = self.context['request'].user.profile

        for attr, value in data.items():
            if (attr == 'chest' or attr == 'waist' or attr == 'hip' or
                    attr == 'leg' or attr == 'bicep'):
                if profile.measurement_system == 'METRIC':
                    value = Distance(cm=value)
                else:
                    value = Distance(inch=value)
                setattr(instance, attr, value)
            if attr == 'bodyweight':
                if profile.measurement_system == 'METRIC':
                    value = Weight(kg=value)
                else:
                    value = Weight(lb=value)
                setattr(instance, attr, value)

        instance = self.upload_files(instance, data)

        instance.save()

        return instance

    def upload_files(self, instance, data):
        """Upload files.

        If file exists then delete from cloudinary first.
        """
        if 'front_image_url' in data:
            if instance.front_image_url:
                cloudinary.uploader.destroy(instance.front_image_url.public_id,
                                            invalidate=True)
            response = cloudinary.uploader.upload(
                data['front_image_url'],
                folder="bodymeasurecontrol/measures",
                transformation={
                    "if": "height > 500",
                    "height": 500,
                    "crop": "scale"
                }
            )
            instance.front_image_url = cloudinary.CloudinaryImage(
                public_id=response['public_id']
            )

        if 'side_image_url' in data:
            if instance.side_image_url:
                cloudinary.uploader.destroy(instance.side_image_url.public_id,
                                            invalidate=True)
            response = cloudinary.uploader.upload(
                data['side_image_url'],
                folder="bodymeasurecontrol/measures",
                transformation={
                    "if": "height > 500",
                    "height": 500,
                    "crop": "scale"
                }
            )
            instance.side_image_url = cloudinary.CloudinaryImage(
                public_id=response['public_id'])

        if 'back_image_url' in data:
            if instance.back_image_url:
                cloudinary.uploader.destroy(instance.back_image_url.public_id,
                                            invalidate=True)
            response = cloudinary.uploader.upload(
                data['back_image_url'],
                folder="bodymeasurecontrol/measures",
                transformation={
                    "if": "height > 500",
                    "height": 500,
                    "crop": "scale"
                }
            )
            instance.back_image_url = cloudinary.CloudinaryImage(
                public_id=response['public_id'])

        return instance


class EntryMeasureCreateModelSerializer(EntryMeasureModelSerializer):
    """EntryMeasure serializer for creation."""

    date_measure = serializers.DateField(
        required=False,
        default=timezone.now().date
    )

    def validate_date_measure(self, date):
        """Check if exists an entryMeasure for given date and user."""
        if EntryMeasure.objects.filter(
            user=self.context['request'].user,
            date_measure=date
        ).count() == 1:
            if date == timezone.now().date():
                raise serializers.ValidationError(
                    "There is already a measure for the given today date"
                )
            raise serializers.ValidationError(
                "There is already a measure for the given date"
            )

        return date

    def create(self, data):
        """Entrymeasure create."""
        user = self.context['request'].user
        profile = user.profile

        entrymeasure = EntryMeasure()
        for attr, value in data.items():
            if (attr == 'chest' or attr == 'waist' or attr == 'hip' or
                    attr == 'leg' or attr == 'bicep'):
                if profile.measurement_system == 'METRIC':
                    value = Distance(cm=value)
                else:
                    value = Distance(inch=value)
                setattr(entrymeasure, attr, value)
            if attr == 'bodyweight':
                if profile.measurement_system == 'METRIC':
                    value = Weight(kg=value)
                else:
                    value = Weight(lb=value)
                setattr(entrymeasure, attr, value)

        entrymeasure.user = user
        entrymeasure.profile = profile
        if 'date_measure' in data:
            entrymeasure.date_measure = data['date_measure']

        entrymeasure = self.upload_files(entrymeasure, data)
        entrymeasure.save()

        return entrymeasure
