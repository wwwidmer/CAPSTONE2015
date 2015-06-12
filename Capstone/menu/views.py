from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from menu.models import Menu, FoodItem, Review, FoodType
from menu.forms import ReviewForm
from django.db.models import Q
from math import floor
import re, datetime

def index(request):
    context = {}
    return render_to_response("index.html",context)

'''
Render menu - get menu by id
    Then get all relation on food items
Render food - get food by id
    Then get all relation on reviews
'''
def render_menu(request,m_id):
    menu = Menu.objects.get(id=m_id)
    food = FoodItem.objects.all().filter(title__id=m_id)
    context = {'menu':menu, 'food':food}
    return render_to_response("menu.html",context)

def render_food(request,f_id):
    food = FoodItem.objects.get(id=f_id)
    review = Review.objects.all().filter(name__id=f_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            render_new_review(form,request,f_id)
    else:
        form = ReviewForm()
    context = {'food':food, 'reviews':review,'form':form, 'avg':get_Average(f_id)}
    return render_to_response("food.html",context,context_instance=RequestContext(request))

def render_new_review(form,request, f_id):
    instance = form.save(commit=False)
    instance.name = FoodItem.objects.get(id=f_id)
    instance.title = instance.name.title
    instance.type = instance.name.type
    instance.date = datetime.datetime.now()
    instance.save()
    return HttpResponseRedirect("/")



# In the future this will grab the top 20 or so 'Best Rated' items.
# Best rated = function of how many ratings and average rating
def render_browse_top_menu(request):
    menus = Menu.objects.all().order_by('-id')
    context = {'menus':menus}
    return render_to_response("menu.html",context)

def render_browse_type_food(request,type):
    pass

def render_browse_loc_menu(request,loc):
    pass

# Grab a list from food types most similar to food
# Right now it just grabs food items of same type
# Future would be to grab several types, lat / long, name
# UNTESTED
def get_similar(food_type_id):
    food = FoodItem.objects.all().filter(type__id=food_type_id)
    return food

# Get all reviews of food ratings and average
# UNTESTED
def get_Average(food_id):
    try:
        reviews = Review.objects.all().filter(name_id=food_id)
        total = 0
        for x in reviews:
            total = x.rating + total
        return floor((total / reviews.count()))
    except ZeroDivisionError:
        return 0


#
def render_search(request):
    query_string = ''
    menu = ''
    food = ''
    found = None
    if('search' in request.GET) and request.GET['search'].strip():
        query_string = request.GET.get('search')
        mentry = get_query(query_string,['title'])
        fentry = get_query(query_string,['name'])
        menu = Menu.objects.filter(mentry).order_by('-id')
        food = FoodItem.objects.filter(fentry).order_by('-id')

    context = {"GET":query_string,'menu':menu,'food':food}
    return render_to_response("search.html",context)

# search function
def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
	query = None
	terms = normalize_query(query_string)
	for t in terms:
		or_query = None
		for field_name in search_fields:
			q = Q(**{"%s__icontains" % field_name : t})
			if or_query is None:
				or_query = q
			else:
				or_query = or_query | q
		if query is None:
			query = or_query
		else:
			query = query & or_query
	return query
