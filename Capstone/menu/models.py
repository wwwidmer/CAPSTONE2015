from django.db import models

# Create your models here. See Issue on github for database schema
# class nameOfModel(models.Model): ....


class Menu(models.Model):
    title = models.CharField(max_length=200)

class FoodItem(models.Model):
    type = ""
    dishname = models.CharField(max_length=200)
    menu = models.ForeignKey(Menu, default=None)

class Review(models.Model):
    #reviewer = models.CharField(max_length=200)
    food = models.ForeignKey(FoodItem, default=None)
    rating = models.IntegerField(default=0)
    comment = models.CharField(max_length=500)
