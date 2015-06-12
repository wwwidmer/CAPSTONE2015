__author__ = 'wwidmer'

from menu.models import Review, FoodItem
from django import forms

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating','review']


class FoodForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name','type']
