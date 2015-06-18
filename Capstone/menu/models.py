from django.db import models
from PIL import Image
from django.core.validators import MinValueValidator, MaxValueValidator
from math import floor


#class MenuLogo(models.Model):
#    logo = models.ImageField(upload_to='media/menu_logo')
#    def __self__(self):
#        return logo
#This model is utilized to setup a new menu name (eg restaurant name)
class Menu(models.Model):
    title = models.CharField(max_length=30,default = None)
    logo = models.ImageField(upload_to='media',blank=True,editable=True,verbose_name='logo')
    def __str__(self): #This returns the value of title in the admin view
        return self.title

    class Meta: #defines menu admin default name
        verbose_name = 'Menu Management'
        verbose_name_plural = 'Menu Management'
#:Image Resizer below for logo
    def __unicode__(self):
        return "{0}".format(self.logo)

    def save(self):
        if not self.logo:
            self.logo = 'media/default.png'

        super(Menu, self).save()
        logo = Image.open(self.logo)
        size = ( 100, 100)
        logo = logo.resize(size, Image.ANTIALIAS)
        logo.save(self.logo.path)
#:End Image Resizer for logo
#This model is utilized to organize different dish types on a menu
class FoodType(models.Model):
    type = models.CharField(max_length=30,default=None)
    def __str__(self):
        return self.type
    class Meta:
        verbose_name = 'Category for Food Type'
        verbose_name_plural = 'Category for Food Type'

#This model is setup with a many items to one menu and many items to one type organization
class FoodItem(models.Model):
    title = models.ForeignKey(Menu, default=None)
    logo = models.ImageField(upload_to='media',blank=True,editable=True,verbose_name='logo')
    type = models.ForeignKey(FoodType,default=None)
    name = models.CharField(max_length=30)
    average = models.IntegerField(default=0)

    def __str__(self):
        return self.name
#:Image Resizer below for logo
    def __unicode__(self):
        return "{0}".format(self.logo)

    def save(self):
        if not self.logo:
            self.logo='media/default.png'

        super(FoodItem, self).save()
        logo = Image.open(self.logo)
        size = ( 100, 100)
        logo = logo.resize(size, Image.ANTIALIAS)
        logo.save(self.logo.path)
#:End Image Resizer for menu.logo


# Upon further inspection the relationship to Menu from Review isn't really warranted but I remove it.
# Since we need Reviews based on Food its not necessary to filter them through menu
# We can just do MenuID->FoodID->Review.
# - William
class Review(models.Model):
    title = models.ForeignKey(Menu, default=None) #One menu points to many reviews
    logo = models.ImageField(upload_to='media',blank=True,editable=True,verbose_name='logo')
    type = models.ForeignKey(FoodType, default=None)#One dish_type points to many reviews
    name = models.ForeignKey(FoodItem,default=None)#One dish points to many reviews
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(5)])
    date = models.DateField('Published on')
    review = models.TextField(max_length=200, default=None)
    #average = models.IntegerField(default=0)
    def __str__(self):
        return self.review
#:Image Resizer below for logo
    def __unicode__(self):
        return "{0}".format(self.logo)

    def save(self):
        if not self.logo:
            self.logo='media/default.png'

        super(Review, self).save()
        logo = Image.open(self.logo)
        size = ( 100, 100)
        logo = logo.resize(size, Image.ANTIALIAS)
        logo.save(self.logo.path)
#:End Image Resizer for menu.logo


# Get all reviews of food ratings and average, total average of menu
def get_Average(food_id):
    try:
        reviews = Review.objects.all().filter(name_id=food_id)
        total = 0
        for x in reviews:
            total = x.rating + total
        return floor((total / reviews.count()))

    except ZeroDivisionError:
       return 0
