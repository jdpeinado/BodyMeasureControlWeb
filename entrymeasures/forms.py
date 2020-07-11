"""EntryMeasures forms."""

# Django
from django import forms

# Models
from entrymeasures.models import EntryMeasure
from django_measurement.models import MeasurementField

# Utils
from measurement.measures import Weight,Distance
import cloudinary


class CompareEntryMeasureForm(forms.Form):
    """Entrymeasures to compare"""

    date_measure1 = forms.DateField()
    date_measure2 = forms.DateField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CompareEntryMeasureForm, self).__init__(*args, **kwargs)

    def clean_date_measure1(self):
        """Verify date measures 1 exists"""
        date_measure1 = self.cleaned_data['date_measure1']
        if EntryMeasure.objects.filter(active=True, user=self.request.user,date_measure=date_measure1).count()==1:
            return date_measure1
        raise forms.ValidationError('There is no measure in that date.')
    
    def clean_date_measure2(self):
        """Verify date measures 2 exists"""
        date_measure2 = self.cleaned_data['date_measure2']
        if EntryMeasure.objects.filter(active=True, user=self.request.user,date_measure=date_measure2).count()==1:
            return date_measure2
        raise forms.ValidationError('There is no measure in that date.')



class UpdateEntryMeasureForm(forms.ModelForm):
    """EntryMeasure update model form."""

    clear_front_image = forms.BooleanField(required=False)
    clear_side_image = forms.BooleanField(required=False)
    clear_back_image = forms.BooleanField(required=False)

    chest = forms.DecimalField(max_digits=4, decimal_places=1)
    waist = forms.DecimalField(max_digits=4, decimal_places=1)
    hip = forms.DecimalField(max_digits=4, decimal_places=1)
    leg = forms.DecimalField(max_digits=4, decimal_places=1)
    bicep = forms.DecimalField(max_digits=4, decimal_places=1)
    bodyweight = forms.DecimalField(max_digits=4, decimal_places=1)

    class Meta:
        """Update form field"""

        model = EntryMeasure
        fields = (
            'user', 
            'profile',  
            'front_image_url',
            'side_image_url',
            'back_image_url',
        )
    
    def save(self):
        """Update a entrymeasure"""
        entrymeasure = self.instance

        if 'delete' in self.data:
            entrymeasure.delete()

            return EntryMeasure()
        else:

            data = self.cleaned_data
            user = data['user']
            profile = data['profile']
            if profile.measurement_system == 'METRIC':
                entrymeasure.bodyweight = Weight(kg=data['bodyweight'])
                entrymeasure.chest = Distance(cm=data['chest'])
                entrymeasure.waist = Distance(cm=data['waist'])
                entrymeasure.hip = Distance(cm=data['hip'])
                entrymeasure.leg = Distance(cm=data['leg'])
                entrymeasure.bicep = Distance(cm=data['bicep'])
            else:
                entrymeasure.bodyweight = Weight(lb=data['bodyweight'])
                entrymeasure.chest = Distance(inch=data['chest'])
                entrymeasure.waist = Distance(inch=data['waist'])
                entrymeasure.hip = Distance(inch=data['hip'])
                entrymeasure.leg = Distance(inch=data['leg'])
                entrymeasure.bicep = Distance(inch=data['bicep'])
            entrymeasure.user = user
            entrymeasure.profile = profile
            
            if 'front_image_url' in self.changed_data:
                if entrymeasure.front_image_url:
                    cloudinary.uploader.destroy(entrymeasure.front_image_url.public_id, invalidate = True)
                if data['front_image_url'].image.size[1] > 500:
                    response = cloudinary.uploader.upload(data['front_image_url'], folder="bodymeasurecontrol/measures", transformation = {"height": 500, "crop": "scale"})
                else:
                    response = cloudinary.uploader.upload(data['front_image_url'], folder="bodymeasurecontrol/measures")
                entrymeasure.front_image_url = cloudinary.CloudinaryImage(public_id=response['public_id'])
            else:
                if data['clear_front_image']:
                    if entrymeasure.front_image_url:
                        cloudinary.uploader.destroy(entrymeasure.front_image_url.public_id, invalidate = True)
                    entrymeasure.front_image_url = None

            if 'side_image_url' in self.changed_data:
                if entrymeasure.side_image_url:
                    cloudinary.uploader.destroy(entrymeasure.side_image_url.public_id, invalidate = True)
                if data['side_image_url'].image.size[1] > 500:
                    response = cloudinary.uploader.upload(data['side_image_url'], folder="bodymeasurecontrol/measures", transformation = {"height": 500, "crop": "scale"})
                else:
                    response = cloudinary.uploader.upload(data['side_image_url'], folder="bodymeasurecontrol/measures")
                entrymeasure.side_image_url = cloudinary.CloudinaryImage(public_id=response['public_id'])
            else:
                if data['clear_side_image']:
                    if entrymeasure.side_image_url:
                        cloudinary.uploader.destroy(entrymeasure.side_image_url.public_id, invalidate = True)
                    entrymeasure.side_image_url = None

            if 'back_image_url' in self.changed_data:
                if entrymeasure.back_image_url:
                    cloudinary.uploader.destroy(entrymeasure.back_image_url.public_id, invalidate = True)
                if data['back_image_url'].image.size[1] > 500:
                    response = cloudinary.uploader.upload(data['back_image_url'], folder="bodymeasurecontrol/measures", transformation = {"height": 500, "crop": "scale"})
                else:
                    response = cloudinary.uploader.upload(data['back_image_url'], folder="bodymeasurecontrol/measures")
                entrymeasure.back_image_url = cloudinary.CloudinaryImage(public_id=response['public_id'])
            else:
                if data['clear_back_image']:
                    if entrymeasure.back_image_url:
                        cloudinary.uploader.destroy(entrymeasure.back_image_url.public_id, invalidate = True)
                    entrymeasure.back_image_url = None

            entrymeasure.save()

            return entrymeasure

class EntryMeasureForm(forms.ModelForm):
    """EntryMeasure model form."""

    chest = forms.DecimalField(max_digits=4, decimal_places=1)
    waist = forms.DecimalField(max_digits=4, decimal_places=1)
    hip = forms.DecimalField(max_digits=4, decimal_places=1)
    leg = forms.DecimalField(max_digits=4, decimal_places=1)
    bicep = forms.DecimalField(max_digits=4, decimal_places=1)
    bodyweight = forms.DecimalField(max_digits=4, decimal_places=1)

    front_image_url = forms.ImageField(
        required=False,
        widget=forms.FileInput()
    )
    side_image_url = forms.ImageField(
        required=False,
        widget=forms.FileInput()
    )
    back_image_url = forms.ImageField(
        required=False,
        widget=forms.FileInput()
    )

    class Meta:
        """Form settings."""

        model = EntryMeasure
        fields = (
            'user', 
            'profile',  
            'date_measure',
        )
    
    def save(self):
        """Save a entrymeasure"""
        data = self.cleaned_data

        user = data['user']
        profile = data['profile']
        entrymeasure = EntryMeasure()
        if profile.measurement_system == 'METRIC':
            entrymeasure.bodyweight = Weight(kg=data['bodyweight'])
            entrymeasure.chest = Distance(cm=data['chest'])
            entrymeasure.waist = Distance(cm=data['waist'])
            entrymeasure.hip = Distance(cm=data['hip'])
            entrymeasure.leg = Distance(cm=data['leg'])
            entrymeasure.bicep = Distance(cm=data['bicep'])
        else:
            entrymeasure.bodyweight = Weight(lb=data['bodyweight'])
            entrymeasure.chest = Distance(inch=data['chest'])
            entrymeasure.waist = Distance(inch=data['waist'])
            entrymeasure.hip = Distance(inch=data['hip'])
            entrymeasure.leg = Distance(inch=data['leg'])
            entrymeasure.bicep = Distance(inch=data['bicep'])
        entrymeasure.user = user
        entrymeasure.profile = profile
        entrymeasure.date_measure = data['date_measure']
        if data['front_image_url']:
            if data['front_image_url'].image.size[1] > 500:
                response = cloudinary.uploader.upload(data['front_image_url'], folder="bodymeasurecontrol/measures", transformation = {"height": 500, "crop": "scale"})
            else:
                response = cloudinary.uploader.upload(data['front_image_url'], folder="bodymeasurecontrol/measures")
            entrymeasure.front_image_url = cloudinary.CloudinaryImage(public_id=response['public_id'])
        if data['side_image_url']:
            if data['side_image_url'].image.size[1] > 500:
                response = cloudinary.uploader.upload(data['side_image_url'], folder="bodymeasurecontrol/measures", transformation = {"height": 500, "crop": "scale"})
            else:
                response = cloudinary.uploader.upload(data['side_image_url'], folder="bodymeasurecontrol/measures")
            entrymeasure.side_image_url = cloudinary.CloudinaryImage(public_id=response['public_id'])
        if data['back_image_url']:
            if data['back_image_url'].image.size[1] > 500:
                response = cloudinary.uploader.upload(data['back_image_url'], folder="bodymeasurecontrol/measures", transformation = {"height": 500, "crop": "scale"})
            else:
                response = cloudinary.uploader.upload(data['back_image_url'], folder="bodymeasurecontrol/measures")
            entrymeasure.back_image_url = cloudinary.CloudinaryImage(public_id=response['public_id'])

        entrymeasure.save()

        return entrymeasure