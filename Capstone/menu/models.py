from django.db import models

# Create your models here. See Issue on github for database schema
# class nameOfModel(models.Model): ....
#This model is utilized to setup a new menu name (eg restaurant name)
class Menu(models.Model):
    menu_title = models.CharField(max_length=200)
    def __str__(self): #This returns the value of title in the admin view
        return self.menu_title

#This model is utilized to organize different dish types on a menu
class FoodType(models.Model):
    dish_type = models.CharField(max_length=10,default=None)
    def __str__(self):
        return self.dish_type
#This model is setup with a many items to one menu and many items to one type organization
class FoodItem(models.Model):
    menu_title = models.ForeignKey(Menu, default=None) #requires a specific menu
    dish_type = models.ForeignKey(FoodType,default=None)#requires a specific type of food item
    dish_name = models.CharField(max_length=200) #then define the dishname to assign to this menu/type
    def __str__(self):
        return self.dish_name
#This model will display a chosen menu and the contents
#Add rating module 1-5 like footype
class Review(models.Model):
    #Keep in mind the many to one relationship in these cases imply
    #that you could access reviews as a whole or use filters based on
    #the variables below e.g. Menu Title->All Reviews or more Specific
    #would be Menu Title->Dish Name->All reviews
    menu_title = models.ForeignKey(Menu, default=None) #One menu points to many reviews
    dish_type = models.ForeignKey(FoodType, default=None)#One dish_type points to many reviews
    dish_name = models.ForeignKey(FoodItem,default=None)#One dish points to many reviews
    review_date = models.DateField('Published on')
    #Menu.objects.all().filter(title=m_id)
    reviews = models.CharField(max_length=200, default=None)
    def __str__(self):
        return self.reviews
