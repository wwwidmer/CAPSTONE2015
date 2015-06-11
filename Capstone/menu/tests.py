from django.test import TestCase
from menu.models import *
from menu.views import *

# Create your tests here.
# William will code testing when appropriate

class MenuTestCase(TestCase):
    def setUp(self):
        Menu.objects.create(title="Test1")
        Menu.objects.create(title="Test2")
        Menu.objects.create(title="Test3")
    # Test we can get objects by title then assert their IDs are unique
    def test_is_unique(self):
        m1 = Menu.objects.get(title="Test1")
        m2 = Menu.objects.get(title="Test2")
        self.assertNotEqual(m1.id,m2.id,"IDs are Unique")
    def test_get_by_ID_or_title(self):
        m1 = Menu.objects.get(title="Test1")
        m2 = Menu.objects.get(id=1)
        self.assertEqual(m1,m2,"ID is unique but can grab the same object by its title")
        self.assertEqual(m1.id,m2.id,"ID is unique but can grab the same object by its title")
        self.assertEqual(m1.title,m2.title,"ID is unique but can grab the same object by its title")


class FoodTestCase(TestCase):
    def setUp(self):
        Menu.objects.create(title="Test1")
        Menu.objects.create(title="Test2")
        FoodItem.objects.create(dishname="TestDish1",menu=Menu.objects.get(title="Test1"))
        FoodItem.objects.create(dishname="TestDish2",menu=Menu.objects.get(title="Test1"))
        FoodItem.objects.create(dishname="TestDish3",menu=Menu.objects.get(title="Test2"))


class ReviewTestcase(TestCase):
    def setUp(self):
        Menu.objects.create(title="Test1")
        FoodItem.objects.create(dishname="TestDish1",menu=Menu.objects.get(title="Test1"))
        Review.ojects.create(food=FoodItem.objects.get(dishname="TestDish1"), rating = 2, comment="TestComment")
        Review.ojects.create(food=FoodItem.objects.get(dishname="TestDish1"), rating = 4, comment="TestComment")



class SearchTestCase(TestCase):
    pass