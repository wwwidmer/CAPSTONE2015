from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse
from django.template import RequestContext
from menu.models import Menu, FoodItem, Review, FoodType, get_Average
from menu.forms import ReviewForm
from django.db.models import Q
from django.core import serializers
import json
from random import randrange, sample
import re, datetime

def test(request):
    return render_to_response('test.html')

def index(request):
    try:
        rand = randrange(0,Menu.objects.all().count())
        menus = Menu.objects.all()[rand]
        frand = randrange(0,FoodItem.objects.all().filter(menuName__id=menus.id).count())
        foods = FoodItem.objects.all().filter(menuName__id=menus.id)[frand]
        rrand = randrange(0,Review.objects.all().filter(foodItemName__id=foods.id).count())
        revs = Review.objects.all().filter(foodItemName__id=foods.id)[rrand]
        avg = get_Average(None,menus.id)
        '''
        rrand = randrange(0,Review.objects.all().count())
        revs = Review.objects.all()[rrand]
        frand = randrange(0,FoodItem.objects.all().filter(foodItemName__id=id).count())
        foods = FoodItem.objects.all().filter(foodItemName__id=id)[frand]
        mrand = randrange(0,Menu.objects.all().filter(foods__menuName=id).count())
        menus = Menu.objects.all().filter(foods_menuName=id)[mrand]
        '''
    except ValueError:
        menus = None
        foods = None
        revs = None
        avg = None

    context = {'rand_menu':menus, 'rand_food':foods, 'rand_rev':revs, 'avg':avg}
    return render_to_response("index.html",context)

def render_search_index(request):
    allTypes = FoodType.objects.all().order_by("type")
    rand = sample(list(allTypes),8)
    context = {'types':rand}
    return render_to_response("search-index.html",context)
'''
Render menu - get menu by id
    Then get all relation on food items
Render food - get food by id
    Then get all relation on reviews
'''
def render_menu(request,m_id):
    try:
        menu = Menu.objects.get(id=m_id)
    except Menu.DoesNotExist:
        raise Http404
    food = FoodItem.objects.all().filter(menuName__id=m_id)
    context = {'menu':menu, 'food':food,'avg':get_Average(None,m_id)}
    return render_to_response("menu.html",context)
'''
Request method for comment form.
if POST (ie we've submitted a form from this page)
handle the form to add a new review object to the database
'''
def render_food(request,f_id):
    try:
        food = FoodItem.objects.get(id=f_id)
        setattr(food,'rating',get_Average(f_id,None))
        food.save()
    except FoodItem.DoesNotExist:
        raise Http404
    review = Review.objects.all().filter(foodItemName__id=f_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST,request.FILES)
        if form.is_valid():
            return render_new_review(form,request,f_id)
    else:
        form = ReviewForm()
    context = {'food':food, 'reviews':review,'form':form, 'avg':get_Average(f_id,None)}
    return render_to_response("food.html",context,context_instance=RequestContext(request))


'''
render new review
get information from the POST request pertaining to adding a new comment
get fooditem related to this with .get and using an ID
set all data without a default and save to database
return a redirect to the same page.
'''

def render_new_review(form, request, f_id):
    instance = form.save(commit=False)
    instance.foodItemName = FoodItem.objects.get(id=f_id)
    instance.createdBy = form.cleaned_data['createdBy']
    instance.logo = form.cleaned_data['logo']
    instance.rating = form.cleaned_data['rating']
    instance.createdOn = datetime.datetime.now()
    instance.save()
    return HttpResponseRedirect("")

# In the future this will grab the top 20 or so 'Best Rated' items.
# Best rated = function of how many ratings and average rating
def render_browse_top_menu(request):
    menus = Menu.objects.all()
    sorted(menus,key=lambda x: (get_Average(None,x.id)))
    context = {'menus':menus}
    return render_to_response("menu.html",context)
def render_browse_type_index(request):
    foodType = FoodType.objects.all().order_by("type")
    context = {'foodTypes':foodType}
    return render_to_response("food.html",context)

def render_browse_type_food(request,t_id):
    fetchFood = FoodItem.objects.filter(type__id=t_id)
    foodType = FoodType.objects.get(id=t_id)
    context = {'foodsAsType':fetchFood,'foodType':foodType}
    return render_to_response("food.html",context)

"""
Not strictly View related functions / helpers / wrappers
"""

# Grab a list from food types most similar to food
# Future would be to grab several types, lat / long, name
def get_similar(food_type_id):
    pass

"""
Search Handlers
"""
def render_search(request):
    query_string = ''
    menu = ''
    food = ''
    found = None
    if('search' in request.GET) and request.GET['search'].strip():
        query_string = request.GET.get('search')
        mentry = get_query(query_string,['title'])
        tentry = get_query(query_string,['type'])
        fentry = get_query(query_string,['dishName'])
        menu = Menu.objects.filter(mentry).order_by('-id')
        food = FoodItem.objects.filter(fentry).order_by('-id')
        type = FoodType.objects.filter(tentry).order_by('-id')

    context = {"GET":query_string,'menu':menu,'food':food,'type':type}
    return render_to_response("search.html",context)

# Search function
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


"""
Ajax handlers
Grab information from the database without reloading webpage
Each Method expects certain URL parameters and throws error if they don't exist
Generally return JSON response
"""

# get food by id
def ajax_get_food_by_id(request):
    if request.is_ajax():
        try:
            if 'fid' in request.GET:
                fid = request.GET.get('fid')
                fetchFood = FoodItem.objects.filter(id=fid)
                data = serializers.serialize('json',fetchFood)
                return JsonResponse(data,safe=False)
            else:
                return HttpResponse("Error using AJAX (check parameters)")
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("You do not have permission to access this webpage")

# get menu by id
def ajax_get_menu_by_id(request):
    if request.is_ajax():
        try:
            if 'mid' in request.GET:
                mid = request.GET.get('mid')
                fetchMenu = Menu.objects.filter(id=mid)
                data = serializers.serialize('json',fetchMenu)
                return JsonResponse(data,safe=False)
            else:
                return HttpResponse("Error using AJAX (check parameters)")
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("You do not have permission to access this webpage")

# Get all reviews associated with food
def ajax_get_review_by_food(request):
    if request.is_ajax():
        try:
            if 'fid' in request.GET:
                fid = request.GET.get('fid')
                fetchReview = Review.objects.filter(FoodItemName__id=fid)
                data = serializers.serialize('json',fetchReview)
                return JsonResponse(data, safe=False)
            else:
                return HttpResponse("Error using AJAX (check parameters)")
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("You do not have permission to access this webpage")

def ajax_get_food_by_menu_id(request):
    if request.is_ajax():
        try:
            if 'mid' in request.GET:
                mid = request.GET.get('mid')
                fetchFood = FoodItem.objects.filter(title__id=mid)
                data = serializers.serialize('json',fetchFood)
                return JsonResponse(data,safe=False)
            else:
                return HttpResponse("Error using AJAX (check parameters)")
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("You do not have permission to access this webpage")

