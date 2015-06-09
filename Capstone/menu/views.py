from django.shortcuts import render_to_response
from menu.models import Menu, FoodItem, Review

def index(request):
    # Get certain models to populate context
    context = {}
    return render_to_response("index.html",context)

def render_menu(request,m_id):
    # get menu by id, get all food associated with
    menu = Menu.objects.all().filter(id=m_id)
    context = {'menu':menu}
    return render_to_response("menu.html",context)

def render_food(request,f_id):
    # get food by id, get all comments associated with
    food = FoodItem.objects.all().filter(f_id=f_id)
    context = {'food':food}
    return render_to_response("food.html",context)

def render_search(request):
    get = request.GET.get('search')
    context = {"GET":get}
    return render_to_response("search.html",context)
