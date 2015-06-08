from django.shortcuts import render_to_response


def index(request):
    # Get certain models to populate context
    context = {}
    return render_to_response("index.html",context)

def render_menu(request):
    # get menu by id, get all food associated with
    pass

def render_food(request):
    # get food by id, get all comments associated with
    pass

def render_search(request):
    # pass url param, GET url param, search somehow
    pass

def render_search_results(request):
    pass
