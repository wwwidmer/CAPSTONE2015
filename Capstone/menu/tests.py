from django.test import TestCase
from django.http import request
from menu.models import Menu, Review, FoodType, FoodItem, get_Average
from menu.views import ajax_get_menu_by_id, ajax_get_food_by_menu_id, ajax_get_review_by_food

class MenuTestCase(TestCase):
    def setUp(self):
        Menu.objects.create(menuName="T1")
        Menu.objects.create(menuName="T2")
    def test_menu_by_id(self):
        getMenu1 = Menu.objects.get(menuName="T1")
        self.assertEqual(getMenu1.id,1, msg="IDs should be predictable")
    def test_menu_unique(self):
        getMenu1 = Menu.objects.get(menuName="T1")
        getMenu2 = Menu.objects.get(menuName="T2")
        self.assertNotEqual(getMenu1.id,getMenu2.id, msg="IDs should be unique")
    def test_ajax_by_menu(self):
        testRequest = request
        testRequest.method='GET'
        testRequest.=True
        testRequest.fid = 1

        ajaxmenu = ajax_get_menu_by_id(testRequest)

class FoodTestCase(TestCase):
    def setUp(self):
        menu1 = Menu.objects.create(menuName="T1")
        type1 = FoodType.objects.create()
        type2 = FoodType.objects.create()
        food1 = FoodItem.objects.create(menuName=menu1)
        food2 = FoodItem.objects.create(menuName=menu1)
    def test_get_food_by_type(self):
        pass
    def test_get_food_by_menu(self):
        pass

class ReviewTestCase(TestCase):
    def setUp(self):
        menu1 = Menu.objects.create(menuName="T1")
        type1 = FoodType.objects.create()
        food1 = FoodItem.objects.create(menuName=menu1)
        rev1 = Review.objects.create(foodItemName=food1,reviewComment = "test0")
        rev2 = Review.objects.create(foodItemName=food1,reviewComment = "test1")
    def test_average_review(self):
        pass
    def test_get_all_reviews_by_food(self):
        pass
    def test_get_all_reviews_by_menu(self):
        pass

class SearchTestCase(TestCase):
    def setUp(self):
        menu1 = Menu.objects.create(menuName="T1")
        menu2 = Menu.objects.create(menuName="T1")
        menu3 = Menu.objects.create(menuName="T1")
        menu4 = Menu.objects.create(menuName="T1")
        '''food1 = FoodItem.objects.create()
        food2 = FoodItem.objects.create()
        food3 = FoodItem.objects.create()
        food4 = FoodItem.objects.create()'''
    def test_search_by_keyword(self):
        pass