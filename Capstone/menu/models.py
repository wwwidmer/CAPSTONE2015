from django.db import models
from PIL import Image
from django.core.validators import MinValueValidator, MaxValueValidator
from math import floor
import uuid
from django.core import signals

'''
Helper Methods
'''
# Get average by ID, takes either food or menu ID passed as parameters (None if not searching)
def get_Average(food_id, menu_id):
    try:
        if menu_id is None:
            reviews = Review.objects.all().filter(foodItemName__id=food_id)
        else:
            reviews = Review.objects.all().filter(foodItemName__menuName=menu_id)
        total = 0
        for x in reviews:
            total = x.rating + total
        return floor((total / reviews.count()))
    except ZeroDivisionError:
        return 0

# Get all items 'below' a certain model and set their state accordingly.
def set_menu_isActive(menu_id, state):
    food = FoodItem.objects.all().filter(menuName=menu_id)
    reviews = Review.objects.all().filter(foodItemName__id=menu_id)
    for item in list(food) + list(reviews):
        item.isActive = state;
        item.save()

def set_food_isActive(food_id,state):
    reviews = Review.objects.all().filter(foodItemName__id=food_id)
    for item in list(reviews):
        item.isActive = state;
        item.save()

#Image resizing function allowing each class inheriting abstract MenuItem to define its own parameters during runtime
def resizeLogo(instance, self, x, y):
    if not self.logo:
        self.logo='default.png'
    super(instance, self).save()
    logo = Image.open(self.logo)
    size = (x, y)
    logo = logo.resize(size, Image.ANTIALIAS)
    logo.save(self.logo.path)

#Define upload path during runtime for each class inheriting abstractMenuItem
def uploadPath(instance, filename):
    return ''.join([instance.uploadPath, filename])

'''
Main Database tables
AbstractMenuItem - All tables will inherit from this - defines basic non redundant information
Menu - Table of inventory information (Where the food is)
FoodType - Table of types (used for grouping FoodItems) * ManyToMany relationship, no common information needed
FoodItem - Table of Stock (Food) Information
Review - Saved Information about Stock
table in our database
'''
class GID(models.Model):
     gid = models.CharField(max_length=100,default='',blank=True)

     def __str__(self):
         return self.gid

class FoodType(models.Model):
    type = models.CharField(max_length=30, default='')
    def __str__(self):
        return self.type
    class Meta:
        verbose_name = 'Category for Food Type'
        verbose_name_plural = 'Category for Food Type'

class abstractMenuItem(models.Model):
    createdOn = models.DateField('Published On', null=True, blank=True)
    createdBy = models.CharField(max_length=30,default='', null=True, blank=True)
    logo = models.ImageField(upload_to=uploadPath, blank=True, editable=True, verbose_name='logo')
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    isActive = models.BooleanField(default=True)
    class Meta: #Abstract model, models that inherit this abstractClass do not share data on the same table
        abstract = True

class Menu(abstractMenuItem):
    id = models.UUIDField(primary_key=True,auto_created=True,editable=False)
    menuName = models.CharField(max_length=30, default='')
    gid = models.ManyToManyField(GID,default='',blank=True)
    uploadPath = 'menuLogo/'
    def save(self,force_insert=False,using=None):
        resizeLogo(Menu, self, 50, 50)
        set_menu_isActive(self.id,self.isActive)
    def __str__(self):
        return self.menuName
    class Meta:
        verbose_name = 'Menu Management'
        verbose_name_plural = 'Menu Management'

class FoodItem(abstractMenuItem):
    menuName = models.ForeignKey(Menu, default=None)
    dishName = models.CharField(max_length=30,default='')
    type = models.ManyToManyField(FoodType, default=None)
    uploadPath = 'foodLogo/'
    def save(self,force_insert=False,using=None):
        resizeLogo(FoodItem, self, 50, 50)
        set_food_isActive(self.id,self.isActive)
    def __str__(self):
        return self.dishName

class Review(abstractMenuItem):
    foodItemName = models.ForeignKey(FoodItem, default=None)
    reviewComment = models.TextField(max_length=500, default=None)
    uploadPath = 'reviewLogo/'
    def save(self,force_insert=False,using=None):
        resizeLogo(Review, self, 50, 50)
    def __str__(self):
        return self.reviewComment
