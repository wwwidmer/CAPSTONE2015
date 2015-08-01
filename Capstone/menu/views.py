from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse
from django.template import RequestContext
from menu.models import Menu, FoodItem, Review, FoodType, get_Average, GID
from menu.forms import ReviewForm
from django.db.models import Q
from django.core import serializers
import json
import math
from random import randrange, sample
import re, datetime

def index(request):
    menus = Menu.objects.all().filter(isActive=True)
    try:
        rrand = randrange(0,Review.objects.all().filter(isActive=True).count())
        revs = Review.objects.all().filter(isActive=True)[rrand]
        foods = FoodItem.objects.get(id=revs.foodItemName.id)
        menus = Menu.objects.get(id=foods.menuName.id)
        avg = get_Average(foods.id,None)
    except ValueError:
        menus = None
        foods = None
        revs = None
        avg = None

    context = {'rand_menu':menus, 'rand_food':foods, 'rand_rev':revs, 'avg':avg,menus:'menus'}
    return render_to_response("index.html",context)

def render_search_index(request):
    allTypes = FoodType.objects.all().order_by('type')
    try:
        rand = sample(list(allTypes), 8)
    except:
        rand = None
    context = {'types': rand}
    return render_to_response("search-index.html", context)
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
    food = FoodItem.objects.all().filter(menuName__id=m_id,isActive=True)
    menu = Menu.objects.get(id=m_id)
    mct = menu.type.count()  # Menu Counted Types
    index = 0
    TButton0 = ""
    TButton1 = ""
    TButton2 = ""
    TButton3 = ""
    TButton4 = ""
    TButton5 = ""
    TList0 = None
    TList1 = None
    TList2 = None
    TList3 = None
    TList4 = None
    TList5 = None
    for t in menu.type.all():
        if index is 0:
            TButton0 = "All"
            TList0 = FoodItem.objects.all().filter(menuName__id=m_id,isActive=True)
            TButton1 = t
            TList1 = FoodItem.objects.all().filter(type=t)
        elif index is 1:
            TButton2 = t
            TList2 = FoodItem.objects.all().filter(type=t)
        elif index is 2:
            TButton3 = t
            TList3 = FoodItem.objects.all().filter(type=t)
        elif index is 3:
            TButton4 = t
            TList4 = FoodItem.objects.all().filter(type=t)
        elif index is 4:
            TButton5 = t
            TList5 = FoodItem.objects.all().filter(type=t)
        index += 1


    context = {'menu':menu, 'food':food,'avg':get_Average(None,m_id),
               'TB0':TButton0,'TB1':TButton1,'TB2':TButton2,'TB3':TButton3,'TB4':TButton4,'TB5':TButton5,
               'TL0':TList0,'TL1':TList1,'TL2':TList2,'TL3':TList3,'TL4':TList4,'TL5':TList5}
    return render_to_response("menu.html",context)

def render_menu_by_gid(request,g_id,name="menu"):
    name = name.replace('-', ' ')  # deslug
    try:
        menu = Menu.objects.get(menuName=name)#checking for existing menu
        try:
            GID.objects.get(gid=g_id) #checking for existing GID (they're unique)
        except GID.DoesNotExist:
            menu = add_menu_gid(g_id, menu) #adding this GID to this menu (passes the menu, modifies it and returns)
    except Menu.DoesNotExist:
        menu = create_menu_by_gid(g_id, name)#create new menu, add gid and return this menu
    m_id = menu.id
    food = FoodItem.objects.all().filter(menuName__id=m_id,isActive=True)
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
    review = Review.objects.all().filter(foodItemName__id=f_id,isActive=True)
    similar = get_similar(f_id)
    menuFood = get_menu_food_random(food.menuName)
    if request.method == 'POST':
        form = ReviewForm(request.POST,request.FILES)
        if form.is_valid():
            return render_new_review(form,request,f_id)
    else:
        form = ReviewForm()
    context = {'food':food, 'reviews':review,'form':form, 'avg':get_Average(f_id,None),'similar':similar,'menuFood':menuFood}
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
    menu = FoodItem.objects.get(id=f_id)
    instance.menuName = menu.menuName
    instance.foodItemName = FoodItem.objects.get(id=f_id)
    instance.createdBy = form.cleaned_data['createdBy']
    instance.logo = form.cleaned_data['logo']
    instance.rating = form.cleaned_data['rating']
    instance.isActive = True
    instance.createdOn = datetime.datetime.now()
    instance.save()
    return HttpResponseRedirect("")

# In the future this will grab the top 20 or so 'Best Rated' items.
# Best rated = function of how many ratings and average rating
def render_browse_top_menu(request):
    menus = Menu.objects.all().filter(isActive=True)
    sorted(menus,key=lambda x: (get_Average(None,x.id)))
    context = {'menus':menus}
    return render_to_response("menu.html",context)
def render_browse_type_index(request):
    foodType = FoodType.objects.all().order_by("type")
    context = {'foodTypes':foodType}
    return render_to_response("food.html",context)
def render_browse_type_food(request,t_id):
    fetchFood = FoodItem.objects.filter(type__id=t_id,isActive=True)
    foodType = FoodType.objects.get(id=t_id)
    context = {'foodsAsType':fetchFood,'foodType':foodType}
    return render_to_response("food.html",context)

"""
Not strictly View related functions / helpers / wrappers
"""

# Grab a list from food types most similar to food
# Future would be to grab several types, lat / long, name, etc
def get_similar(food_id):
    similar = []
    food = FoodItem.objects.get(id=food_id)
    for x in food.type.all():
        similar.append(x.id)
    similarFood = FoodItem.objects.filter(type__id__in=similar).distinct()
    return similarFood

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
        mentry = get_query(query_string,['menuName'])
        tentry = get_query(query_string,['type'])
        fentry = get_query(query_string,['dishName'])
        menu = Menu.objects.filter(mentry,isActive=True).order_by('-id')
        food = FoodItem.objects.filter(fentry,isActive=True).order_by('-id')
        type = FoodType.objects.filter(tentry).order_by('-id')

    context = {"GET":query_string,'menu':menu,'food':food,'type':type,'keyword':query_string}
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

# Created a new menu if gid does not exist
def create_menu_by_gid(g_id, menuName):
    createdOn = datetime.datetime.now()
    isActive = True
    createdBy = "auto"
    newMenu = Menu.objects.create(menuName=menuName,createdOn=createdOn,isActive=isActive,createdBy=createdBy)
    newMenu.save()
    try:
        GID.objects.get(gid=g_id)
    except GID.DoesNotExist:
        add_menu_gid(g_id, newMenu)
        menuGID= GID.objects.get(gid=g_id)
    except GID.DoesNotExist:
        menuGID = add_menu_gid(g_id, newMenu)
        newMenu.gid.add(menuGID)
    return newMenu

def add_menu_gid(g_id, newMenu):
    menuGID = GID.objects.create(gid=g_id)
    menuGID.save()
    newMenu.gid.add(menuGID)
    return newMenu
def get_menu_food_random(menuId):
    food = list(FoodItem.objects.filter(menuName=menuId))
    foodSample = sample(food,math.ceil(len(food)/4))
    return foodSample

"""
Ajax handlers
Grab information from the database without reloading webpage
Each Method expects certain URL parameters and throws error if they don't exist
Generally return JSON response
"""

def ajax_get_search(request):
    if request.is_ajax():
        try:
            query_string=""
            if 'search' in request.GET:
                query_string = request.GET.get('search')
                mentry = get_query(query_string,['menuName'])
                fentry = get_query(query_string,['dishName'])
                menu = Menu.objects.filter(mentry,isActive=True).order_by('?')[:10]
                food = FoodItem.objects.filter(fentry,isActive=True).order_by('?')[:10]
                data = serializers.serialize('json',list(menu)+list(food))
                return JsonResponse(data,safe=False)
            else:
                return HttpResponse("Error using AJAX (check params)")
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("You do not have permission to access this webpage")


# get food by id
def ajax_get_food_by_id(request):
    if request.is_ajax():
        try:
            if 'fid' in request.GET:
                fid = request.GET.get('fid')
                fetchFood = FoodItem.objects.filter(id=fid,isActive=True)
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
                fetchMenu = Menu.objects.filter(id=mid,isActive=True)
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
                fetchReview = Review.objects.filter(FoodItemName__id=fid,isActive=True)
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
                fetchFood = FoodItem.objects.filter(menuName__id=mid,isActive=True)
                data = serializers.serialize('json',fetchFood)
                return JsonResponse(data,safe=False)
            else:
                return HttpResponse("Error using AJAX (check parameters)")
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("You do not have permission to access this webpage")

def ajax_add_menu_by_gid(request):
    if request.is_ajax():
        if 'gid' in request.GET:
            ngid = request.GET.get('gid')
        else:
            return HttpResponse("Error")
        try:
            Menu.objects.get(gid=ngid)
            return HttpResponse("Already Exists, why are you here?")
        except GID.DoesNotExist:
            menuName = "newmenu"
            createdOn = datetime.datetime.now()
            isActive = True
            createdBy = "auto"
            newMenu = Menu.objects.create(menuName=menuName,gid=ngid,createdOn=createdOn,isActive=isActive,createdBy=createdBy)
            return HttpResponse("Item: "+ngid+":"+menuName+" added to database.")
    else:
        return HttpResponse("You do not have permission to access this webpage")