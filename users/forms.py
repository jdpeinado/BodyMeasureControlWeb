"""Users forms"""

# Django
from django import forms

# Models
from django.contrib.auth.models import User
from users.models import Profile
from django_measurement.forms import MeasurementField
from entrymeasures.models import EntryMeasure

# Forms
from cloudinary.forms import CloudinaryFileField    

# Utils
from measurement.measures import Weight, Distance
import decimal
import cloudinary


class SignupForm(forms.Form):
    """Sign up form."""

    username = forms.CharField(min_length=4, max_length=50)

    password = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput()
    )
    password_confirmation = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput()
    )

    first_name = forms.CharField(min_length=2, max_length=50)
    last_name = forms.CharField(min_length=2, max_length=50)

    email = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.EmailInput()
    )

    def clean_username(self):
        """Username must be unique."""
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError('Username is already in use.')
        return username

    def clean(self):
        """Verify password confirmation match."""
        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Passwords do not match.')

        return data

    def save(self):
        """Create user and profile."""
        data = self.cleaned_data
        data.pop('password_confirmation')

        user = User.objects.create_user(**data)
        profile = Profile(user=user)
        profile.save()

class UpdateProfileForm(forms.Form):
    """Update profile form."""

    picture = forms.ImageField(
        required=False,
        widget=forms.FileInput()
    )

    height = forms.DecimalField(max_digits=4, decimal_places=2)

    CHOICES=[(tag, tag.value) for tag in Profile.UnitMeasurement]
    measurement_system = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    country_code = forms.CharField(max_length=2)

    def save(self, profile):
        """Update a profile"""
        data = self.cleaned_data

        profile.measurement_system = data['measurement_system']
        if profile.measurement_system == 'METRIC':
            profile.height = Distance(m=data['height'])
        else:
            profile.height = Distance(ft=data['height'])
        profile.country_code = data['country_code']

        if data['picture']:
            cloudinary.uploader.destroy(profile.picture.public_id, invalidate = True)
            response = cloudinary.uploader.upload(data['picture'], folder="bodymeasurecontrol/users", transformation = {"height": 300, "crop": "scale"})
            profile.picture = cloudinary.CloudinaryImage(public_id=response['public_id'])
        profile.save()

        
        