from django.db import models
from PIL import Image
from django.core.validators import MinValueValidator, MaxValueValidator
from math import floor

'''
Main Database tables
AbstractMenuItem - All tables will inherit from this - defines basic non redundant information
Menu - Table of inventory information (Where the food is)
FoodType - Table of types (used for grouping FoodItems)
FoodItem - Table of Stock (Food) Information
Review - Saved Information about Stock
'''

class AbstractMenuItem(models.Model):
    createdOn = models.DateTimeField()
    createdBy = models.CharField()
    isActive = models.BooleanField()
    readOnlyName = models.CharField()
    description = models.CharField()
    logo = models.ImageField()

    def __str__(self):
        return self.readOnlyName

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        pass
    class Meta:
        pass



class Menu(AbstractMenuItem):
    title = models.CharField(max_length=30,default = None)
    logo = models.ImageField(upload_to='menu_logo',blank=True,editable=True,verbose_name='logo')
    def __str__(self):
        '{0}'.format(self.logo)
        return self.title
    class Meta:
        verbose_name = 'Menu Management'
        verbose_name_plural = 'Menu Management'
    def save(self,force_insert=False,force_update=False,using=None):
        if not self.logo: #check for an image else assign a default
            self.logo = 'default.png'
        super(Menu, self).save()
        logo = Image.open(self.logo)
        size = ( 100, 100)
        logo = logo.resize(size, Image.ANTIALIAS)
        logo.save(self.logo.path)

# Will be replaced to become ManyToMany with FoodItem
class FoodType(AbstractMenuItem):
    type = models.CharField(max_length=30,default=None)
    def __str__(self):
        return self.type
    class Meta:
        verbose_name = 'Category for Food Type'
        verbose_name_plural = 'Category for Food Type'

class FoodItem(AbstractMenuItem):
    menuName = models.ForeignKey(Menu, default=None)
    logo = models.ImageField(upload_to='food_logo',blank=True,editable=True,verbose_name='logo')
    type = models.ForeignKey(FoodType,default=None)
    dishName = models.CharField(max_length=30)
    average = models.IntegerField(default=0)

    def __str__(self):
        '{0}'.format(self.logo)
        return self.dishName
    def save(self):
        if not self.logo:
            self.logo='default.png'

        super(FoodItem, self).save()
        logo = Image.open(self.logo)
        size = (75, 75)
        logo = logo.resize(size, Image.ANTIALIAS)
        logo.save(self.logo.path)

'''
# Upon further inspection the relationship to Menu from Review isn't really warranted but I remove it.
# Since we need Reviews based on Food its not necessary to filter them through menu
# We can just do MenuID->FoodID->Review.
# I've edited to conform to the above 6/29
# - William
'''
class Review(AbstractMenuItem):
    foodItemName = models.ForeignKey(FoodItem,default=None, null=True)
    createdBy = models.CharField(max_length=30,default="No one")
    logo = models.ImageField(upload_to='review_logo',blank=True,editable=True,verbose_name='logo')
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(5)])
    createdOn = models.DateField('Published on')
    reviewComment = models.TextField(max_length=200, default=None)

    def __str__(self):
        '{0}'.format(self.logo)
        return self.reviewComment
    def save(self):
        if not self.logo:
            self.logo='default.png'

        super(Review, self).save()
        logo = Image.open(self.logo)
        size = ( 100, 100)
        logo = logo.resize(size, Image.ANTIALIAS)
        logo.save(self.logo.path)

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
