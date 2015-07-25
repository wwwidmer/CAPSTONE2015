from django.db import models
from django.core.files.storage import default_storage
from django.db.models.signals import pre_delete
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from math import floor
from PIL import Image
from uuid import uuid4
import io
from django.core.files.uploadedfile import SimpleUploadedFile
import os

'''
    Helper Methods
'''

'''
    Image resizing function that generates a thumbnail
'''
def resizeLogo(instance, self, x, y):
    if self.logo.name is not None:
        if 'default.png' in self.logo.name:
            return
    else:
        return

    size = (x, y)
    FILE_EXT = 'png'
    logoIO = io.BytesIO()
    try:
        logo = Image.open(self.logo)
    except self.DoesNotExist:
        return
    logo.thumbnail(size, Image.ANTIALIAS)
    logo.save(logoIO, FILE_EXT)
    logoIO.seek(0)

    suf = SimpleUploadedFile(os.path.split(self.logo.name)[-1], logoIO.read(), content_type=FILE_EXT)
    self.thumbnail.save('%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], FILE_EXT), suf, save=False)
    super(instance, self).save()


'''
    Clean up and resize images if a change is detected, ignore default image
'''
def cleanup(instance, self, x, y):
    try:
        this = instance.objects.get(id=self.id)
    except instance.DoesNotExist:
        this = None
    if this is not None:
        if this.logo != self.logo:
            if default_storage.exists(os.path.join(settings.MEDIA_ROOT,this.logo.name)):
                if 'default.png' not in this.logo.name:
                    os.remove(os.path.join(settings.MEDIA_ROOT,this.logo.name))
            if default_storage.exists(os.path.join(settings.MEDIA_ROOT,this.thumbnail.name)):
                if 'default.png' not in this.thumbnail.name:
                    os.remove(os.path.join(settings.MEDIA_ROOT,this.thumbnail.name))
            resizeLogo(instance, self, x, y)
        return
    resizeLogo(instance, self, x, y)
    return



def deletion(self):
    if default_storage.exists(os.path.join(settings.MEDIA_ROOT,self.logo.name)):
        if 'default.png' not in self.logo.name:
            os.remove(os.path.join(settings.MEDIA_ROOT,self.logo.name))
    if default_storage.exists(os.path.join(settings.MEDIA_ROOT,self.thumbnail.name)):
        if 'default.png' not in self.thumbnail.name:
            os.remove(os.path.join(settings.MEDIA_ROOT,self.thumbnail.name))
    return

'''
    Define upload path during runtime && generate unique filename
'''
def uploadPath(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = '{}{}'.format(uuid4().hex,ext)
    return ''.join([instance.uploadPath, filename])

'''
    Get average by ID, takes either food or menu ID passed as parameters (None if not searching)
'''
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
'''
    Get all items 'below' a certain model and set their state accordingly.
'''
def set_menu_isActive(self):
    try:
        food = FoodItem.objects.all().filter(menuName=self.id)
        reviews = Review.objects.all().filter(foodItemName__id=self.id)
        for item in list(food) + list(reviews):
            item.isActive = self.isActive;
            item.save()
    except self.DoesNotExist:
        return

def set_food_isActive(self):
    try:
        reviews = Review.objects.all().filter(foodItemName__id=self.id)
        for item in list(reviews):
            item.isActive = self.isActive;
            item.save()
    except self.DoesNotExist:
        return

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
    gid = models.CharField(max_length=100,default='', blank=True, unique=True)
    def __str__(self):
         return self.gid

class FoodType(models.Model):
    type = models.CharField(max_length=30, default='', unique=True)
    def __str__(self):
        return self.type
    class Meta:
        verbose_name = 'Category for Food Type'
        verbose_name_plural = 'Category for Food Type'

class abstractMenuItem(models.Model):
    createdOn = models.DateField('Published On', null=True, blank=True)
    createdBy = models.CharField(max_length=30,default='', null=True, blank=True)
    logo = models.ImageField(upload_to=uploadPath, default='default.png', editable=True, verbose_name='logo')
    thumbnail = models.ImageField(upload_to=uploadPath, default='default.png', editable=True, verbose_name='thumbnail')
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    isActive = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Menu(abstractMenuItem):
    menuName = models.CharField(max_length=30, default='')
    gid = models.ManyToManyField(GID,default='',blank=True)
    uploadPath = 'menuLogo/'

    def save(self, *args, **kwargs):
        cleanup(Menu, self,200,200)
        set_menu_isActive(self)
        super(Menu, self).save()
    def delete(self):
        deletion(self)
        RTM = Menu.objects.filter(id=self.id)
        RTM.delete()

    def __str__(self):
        return self.menuName
    class Meta:
        verbose_name = 'Menu Management'
        verbose_name_plural = 'Menu Management'

class FoodItem(abstractMenuItem):
    menuName = models.ForeignKey(Menu, default=None)
    dishName = models.CharField(max_length=30,default='')
    type = models.ManyToManyField(FoodType, default='')
    uploadPath = 'foodLogo/'


    def save(self, *args, **kwargs):
        cleanup(FoodItem, self,100,100)
        set_food_isActive(self)
        super(FoodItem, self).save()
    def delete(self):
        deletion(self)
        RTM = FoodItem.objects.filter(id=self.id)
        RTM.delete()
    def __str__(self):
        return self.dishName

class Review(abstractMenuItem):
    foodItemName = models.ForeignKey(FoodItem, default=None)
    reviewComment = models.TextField(max_length=500, default=None)
    uploadPath = 'reviewLogo/'

    def save(self, *args, **kwargs):
        cleanup(Review, self, 100, 100)
        super(Review, self).save()
    def delete(self):
        deletion(self)
        RTM = Review.objects.filter(id=self.id)
        RTM.delete()
    def __str__(self):
        return self.reviewComment
