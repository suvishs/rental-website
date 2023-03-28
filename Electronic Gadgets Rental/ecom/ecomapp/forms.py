from django import forms
from ecomapp.models import Customer

class ApplicationForm(forms.Form):
    pancard_image_front = forms.ImageField()
    pancard_image_back = forms.ImageField()
    bankstatement = forms.FileField()

    class Meta:
        fields = ['pancard_image_front', 'pancard_image_back', 'bankstatement']
