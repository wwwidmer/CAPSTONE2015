from django.shortcuts import render_to_response
from menu.models import Menu, FoodItem, Review
from django.db.models import Q
import re

def index(request):
    # Get certain models to populate context
    context = {}
    return render_to_response("index.html",context)

def render_menu(request,m_id):
    # get menu by id, get all food associated with
    menu = Menu.objects.all().filter(menu_title=m_id)
    food = FoodItem.objects.all().filter(menu=menu) #accessing menu within FoodItem and limiting food t
    review = Review.objects.all()                   #that foriegn key
    context = {'menu':menu, 'food':food, 'review':review}
    return render_to_response("menu.html",context)

def render_food(request,f_id):
    #get food by id, get all comments associated with
    food = FoodItem.objects.all().filter(f_id=f_id)
    reviews = Review.objects.all().filter(food__id=f_id)
    #context = {'food':food}
    return render_to_response("food.html",context)

def render_search(request):
    #query_string = ''
    #menu = ""
    #food = ""
    found = None
    if('search' in request.GET) and request.GET['search'].strip():
        query_string = request.GET.get('search')
        mentry = get_query(query_string,['menu_title'])
        fentry = get_query(query_string,['food_type'])
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
			q = Q(**{"%s__icontains" % field_name: t})
			if or_query is None:
				or_query = q
			else:
				or_query = or_query | q
		if query is None:
			query = or_query
		else:
			query = query & or_query
	return query