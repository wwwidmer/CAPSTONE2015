from django.db import models

# Create your models here. See Issue on github for database schema
# class nameOfModel(models.Model): ....


class Menu(models.Model):
    title = models.CharField(max_length=200)
class FoodItem(models.Model):
    type = ""
    dishname = models.CharField(max_length=200)
    #reviews =
    def getAverage(self):
        return 1
    def getSimilar(self):
        return 1
class Review(models.Model):
    #reviewer = models.CharField(max_length=200)
    rating = models.IntegerField()
    comment = models.CharField(max_length=500)
