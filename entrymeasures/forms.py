"""EntryMeasures forms."""

# Django
from django import forms

# Models
from entrymeasures.models import EntryMeasure

class EntryMeasureForm(forms.ModelForm):
    """EntryMeasure model form."""

    class Meta:
        """Form settings."""

        model = EntryMeasure
        fields = (
            'user', 
            'profile',  
            'front_image_url',
            'side_image_url',
            'back_image_url',
            'chest',
            'waist',
            'hip',
            'leg',
            'bicep',
            'bodyweight',
        )