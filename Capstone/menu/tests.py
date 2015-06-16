from django.test import TestCase
from menu.models import *
from menu.views import *

# No tests yet, just set up.

class MenuTestCase(TestCase):
    def setUp(self):
        menu1 = Menu.objects.create(title="T1")
        menu2 = Menu.objects.create(title="T2")

class FoodTestCase(TestCase):
    def setUp(self):
        menu1 = Menu.objects.create(title="T1")
        type1 = FoodType.objects.create()
        type2 = FoodType.objects.create()
        food1 = FoodItem.objects.create()
        food2 = FoodItem.objects.create()

class ReviewTestcase(TestCase):
    def setUp(self):
        menu1 = Menu.objects.create(title="T1")
        type1 = FoodType.objects.create()
        food1 = FoodItem.objects.create()
        rev1 = Review.objects.create()
        rev2 = Review.objects.create()


class SearchTestCase(TestCase):
    def setUp(self):
        menu1 = Menu.objects.create(title="T1")
        menu2 = Menu.objects.create(title="T1")
        menu3 = Menu.objects.create(title="T1")
        menu4 = Menu.objects.create(title="T1")
        food1 = FoodItem.objects.create()
        food2 = FoodItem.objects.create()
        food3 = FoodItem.objects.create()
        food4 = FoodItem.objects.create()