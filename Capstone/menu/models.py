from django.db import models
from PIL import Image
from django.core.validators import MinValueValidator, MaxValueValidator
from math import floor

'''
Main Database tables
AbstractMenuItem - All tables will inherit from this - defines basic non redundant information
***Inheritance should only apply to common information
Menu - Table of inventory information (Where the food is)
FoodType - Table of types (used for grouping FoodItems) * ManyToMany relationship, no common redundant information
FoodItem - Table of Stock (Food) Information * FoodItem/MenuName share a 'name'space but review does not
Review - Saved Information about Stock * Reviewcomment is a text field, this should not be passed to each classes
table in our database
'''
#Image resizing function allowing each class inheriting abstractMenuItem to define its own parameters during runtime
def resizeLogo(instance, self, x, y):
        '{0}'.format(self.logo)
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
#abstract multiple table inheritance, models inherit these variables.
#This is data that is shared and joined to each class that inherits this abstract class
#Only one table is created in our database for this abstract class and the one that inherits it.
'''
class abstractMenuItem(models.Model):
    createdOn = models.DateField('Published On', null=True, blank=True) #Disables Requirement of CreatedOn
    createdBy = models.CharField(max_length=30,default='', null=True, blank=True)#Remove blank/null for required
    logo = models.ImageField(upload_to=uploadPath, blank=True, editable=True, verbose_name='logo')
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    isActive = models.BooleanField(default=False)

    class Meta: #Abstract model, models that inherit this abstractClass do not share data on the same table
        abstract = True

class Menu(abstractMenuItem):
    menuName = models.CharField(max_length=30, default='')
    uploadPath = 'menuLogo/'

    def __str__(self):
        resizeLogo(Menu, self, 100, 100)
        return self.menuName

    class Meta:
        verbose_name = 'Menu Management'
        verbose_name_plural = 'Menu Management'

#This is its own table of types
class FoodType(models.Model): #Food Types don't inherit anything, contains single attribute with many to many rel.
    type = models.CharField(max_length=30, default='')

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Category for Food Type'
        verbose_name_plural = 'Category for Food Type'

#This table continues off of the menu table inheriting its variables
class FoodItem(abstractMenuItem):
    menuName = models.ForeignKey(Menu, default=None)
    dishName = models.CharField(max_length=30,default='')
    type = models.ManyToManyField(FoodType, default=None)
    uploadPath = 'foodLogo/'

    def __str__(self):
        resizeLogo(FoodItem, self, 50, 50)
        return self.dishName

'''Misc
# Since we need Reviews based on Food its not necessary to filter them through menu
# We can just do MenuID->FoodID->Review.
'''
class Review(abstractMenuItem):
    foodItemName = models.ForeignKey(FoodItem, default=None)
    reviewComment = models.TextField(max_length=200, default=None)
    uploadPath = 'reviewLogo/'

    def __str__(self):
        resizeLogo(Review, self, 50, 50)
        return self.reviewComment

# Get average by ID, takes either food or menu ID passed as parameters (None if not searching)
def get_Average(food_id, menu_id):
    try:
        if menu_id is None:
            reviews = Review.objects.all().filter(foodItemName__id=food_id)
        else:
            # This gets more complicated without Review linked to Menu... Needs work
            reviews = Review.objects.all().filter(foodItemName__menuName=menu_id)
        total = 0
        for x in reviews:
            total = x.rating + total
        return floor((total / reviews.count()))
    except ZeroDivisionError:
        return 0
