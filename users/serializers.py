"""Users serializers."""

# Django
from django.contrib.auth import password_validation, authenticate

# Models
from users.models import User, Profile

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Utils
from measurement.measures import Distance
import cloudinary


class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer."""

    class Meta:
        """Meta class."""

        model = Profile
        fields = (
            'picture',
            'height',
            'measurement_system',
            'country_code'
        )

    def to_representation(self, instance):
        """

        Transform measurement objects to decimal values for validating.
        Transform cloudinary objects to char values for validating.
        """
        if instance.picture:
            instance.picture = instance.picture.url

        if instance.height:
            if instance.measurement_system == 'METRIC':
                instance.height = round(instance.height.m, 2)
            else:
                instance.height = round(instance.height.ft, 2)

        ret = super().to_representation(instance)

        return ret

    def update(self, instance, data):
        """Update profile keeping in mind height measurement and images
        upload to cloudinary."""

        if 'measurement_system' in data:
            instance.measurement_system = data['measurement_system']
        if 'height' in data:
            if instance.measurement_system == 'METRIC':
                instance.height = Distance(m=data['height'])
            else:
                instance.height = Distance(ft=data['height'])
        if 'country_code' in data:
            instance.country_code = data['country_code']
        if 'picture' in data:
            if instance.picture:
                cloudinary.uploader.destroy(instance.picture.public_id,
                                            invalidate=True)
            response = cloudinary.uploader.upload(
                data['picture'],
                folder="bodymeasurecontrol/users",
                transformation={
                    "if": "height > 300",
                    "height": 300,
                    "crop": "scale"
                }
            )
            instance.picture = cloudinary.CloudinaryImage(
                public_id=response['public_id'])

        instance.save()

        return instance


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer"""

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        """Meta class."""

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'profile'
        )
        read_only_fields = (
            'username',
            'email',
            'profile'
        )


class UserLoginSerializer(serializers.Serializer):
    """User login serializer.

    Handle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet :(')
        self.context['user'] = user
        return data

    def create(self, data):
        """Generate or retrieve new token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class UserSignUpSerializer(serializers.Serializer):
    """User sign up."""

    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate(self, data):
        """Validate password confirmation."""

        if data['password'] != data["password_confirmation"]:
            raise serializers.ValidationError("Passwords don't match")
        password_validation.validate_password(data['password'])

        data.pop('password_confirmation', None)

        return data

    def create(self, data):
        """Create user"""
        user = User.objects.create_user(**data)
        Profile.objects.create(user=user)
        return user
