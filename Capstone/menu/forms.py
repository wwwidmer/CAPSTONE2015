__author__ = 'wwidmer'

from menu.models import Review, FoodItem
from django import forms

class ReviewForm(forms.ModelForm):
    FIVESTAR = [(i,"") for i in range(6)]
    rating = forms.ChoiceField(choices=FIVESTAR, widget=forms.RadioSelect(attrs={'id':'fiveStar'}))
    class Meta:
        model = Review
        fields = ['rating','review']


class FoodForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name','type']
