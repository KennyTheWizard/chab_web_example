from django import forms
from django.forms import ModelForm
from .models import Part

class PartForm(ModelForm):
    class Meta:
        model = Part
        exclude = ['created_at', 'updated_at']

class NewPartForm(forms.Form):
    part_name = forms.CharField(max_length=255, min_length=1)
    part_desc = forms.CharField(widget=forms.Textarea)
    is_divisible = forms.BooleanField(required=False)
    # manufacturer = forms.ModelChoiceField(
    #     Manufacturer.objects.filter(is_active=True), required=False, )
    # new_manufacturer = forms.CharField(max_length=255, required=False)
    # cost = forms.FloatField(min_value=0)
