from django.contrib import admin
from menu.models import Menu, FoodItem, FoodType, Review,Rating  # , organizedMenu

# Register Models are will be edited in the Admin screen
# This may not include all models

class FoodTypeAdmin(admin.ModelAdmin):
    # list_display = ('FType')
    ordering = ['food_type']

class FoodAdmin(admin.StackedInline):
      model = FoodItem
      extra = 0

class Reviews(admin.StackedInline):
     model = Review
     extra = 0

class MenuAdmin(admin.ModelAdmin):
    ordering = ['menu_title']
    fieldsets = [
        (None, {'fields':['menu_title']}),
    ]
    inlines = [FoodAdmin,Reviews]

class RatingAdmin(admin.ModelAdmin):
     ordering = ['rating']

admin.site.register(Menu, MenuAdmin)
admin.site.register(FoodType, FoodTypeAdmin)
admin.site.register(Rating,RatingAdmin)

