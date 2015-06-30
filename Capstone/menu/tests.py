from django.test import TestCase
from menu.models import *
from menu.views import *

class MenuTestCase(TestCase):
    def setUp(self):
        Menu.objects.create(title="T1")
        Menu.objects.create(title="T2")
    def test_menu_by_id(self):
        getMenu1 = Menu.objects.get(title="T1")
        self.assertEqual(getMenu1.id,1, msg="IDs should be predictable")
    def test_menu_unique(self):
        getMenu1 = Menu.objects.get(title="T1")
        getMenu2 = Menu.objects.get(title="T2")
        self.assertNotEqual(getMenu1.id,getMenu2.id, msg="IDs should be unique")
    def test_ajax_by_menu(self):
        pass

class FoodTestCase(TestCase):
    def setUp(self):
        menu1 = Menu.objects.create(title="T1")
        type1 = FoodType.objects.create()
        type2 = FoodType.objects.create()
        food1 = FoodItem.objects.create()
        food2 = FoodItem.objects.create()
    def test_get_food_by_type(self):
        pass
    def test_get_food_by_menu(self):
        pass

class ReviewTestCase(TestCase):
    def setUp(self):
        menu1 = Menu.objects.create(title="T1")
        type1 = FoodType.objects.create()
        food1 = FoodItem.objects.create()
        rev1 = Review.objects.create()
        rev2 = Review.objects.create()
    def test_average_review(self):
        pass
    def test_get_all_reviews_by_food(self):
        pass
    def test_get_all_reviews_by_menu(self):
        pass

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
    def test_search_by_keyword(self):
        pass