from django.db import models

# Create your models here. See Issue on github for database schema
# class nameOfModel(models.Model): ....
#This model is utilized to setup a new menu name (eg restaurant name)
class Menu(models.Model):
    menu_title = models.CharField(max_length=20)
    def __str__(self): #This returns the value of title in the admin view
        return self.menu_title

    class Meta: #defines menu admin default name
        verbose_name = 'Menu Management'
        verbose_name_plural = 'Menu Management'

#This model is utilized to organize different dish types on a menu
class FoodType(models.Model):
    food_type = models.CharField(max_length=10,default=None)
    def __str__(self):
        return self.food_type

    class Meta:
        verbose_name = 'Category for Food Type'
        verbose_name_plural = 'Category for Food Type'
#This model is setup with a many items to one menu and many items to one type organization
class FoodItem(models.Model):
    #One To Many Relations
    menu_title = models.ForeignKey(Menu, default=None) #requires a specific menu
    food_type = models.ForeignKey(FoodType,default=None)#requires a specific type of food item
    #Data
    food_name = models.CharField(max_length=20) #then define the dishname to assign to this menu/type
    def __str__(self):
        return self.food_name

#This Model is utilized to generate a variable rating system e.g. 1-5, 1-10
#This data is defined within the django admin
class Rating(models.Model):
    rating = models.CharField(max_length=1)
    def __str__(self):
        return self.rating

    class Meta:
        verbose_name = 'Rating System'
        verbose_name_plural = 'Rating System'

class Review(models.Model):
    #Keep in mind the many to one relationship in these cases imply
    #that you could access reviews as a whole or use filters based on
    #the variables below e.g. Menu Title->All Reviews or more Specific
    #would be Menu Title->Dish Name->All reviews
    menu_title = models.ForeignKey(Menu, default=None) #One menu points to many reviews
    food_type = models.ForeignKey(FoodType, default=None)#One dish_type points to many reviews
    food_name = models.ForeignKey(FoodItem,default=None)#One dish points to many reviews
    rating = models.ForeignKey(Rating,default=None)
    review_date = models.DateField('Published on')

    review = models.TextField(max_length=200, default=None)
    def __str__(self):
        return self.review
