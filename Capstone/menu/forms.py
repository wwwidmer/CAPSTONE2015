__author__ = 'wwidmer'

from menu.models import Review, FoodItem
from django import forms

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=0,max_value=5)
    class Meta:
        model = Review
        fields = ['rating','review']


class FoodForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name','type']
