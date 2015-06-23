__author__ = 'wwidmer'
from django.shortcuts import HttpResponseRedirect
from menu.models import Review, FoodItem
from django import forms
from django.shortcuts import render

class ReviewForm(forms.ModelForm):
    FIVESTAR = [(i,"") for i in range(6)]
    rating = forms.ChoiceField(choices=FIVESTAR, widget=forms.RadioSelect(attrs={'id':'fiveStar'}))
    logo = forms.ImageField(label='Select a Image',required=False)
    class Meta:
        model = Review
        fields = ['user','rating','logo','review']


class FoodForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name','type']

