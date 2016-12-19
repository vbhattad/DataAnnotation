from django import forms
from .models import classify
#To check from Imagenet
class classify(forms.ModelForm):
    class Meta:
        model = classify