from django.contrib import admin
from menu.models import Menu, FoodItem, FoodType, Review  # , organizedMenu

# Register Models are will be edited in the Admin screen
# This may not include all models

class FoodTypeAdmin(admin.ModelAdmin):
    # list_display = ('FType')
    ordering = ['dish_type']

class FoodAdmin(admin.StackedInline):
      model = FoodItem
      extra = 0

class Reviews(admin.StackedInline):
     model = Review
     extra = 0

class MenuAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['menu_title']}),
    ]
    inlines = [FoodAdmin,Reviews]

class ReviewAdmin(admin.ModelAdmin):
     #fieldsets = [
     #    (None, {'fields': ['m_title']}),
     #    (None, {'fields': ['d_type']})
     #          # {'fields': ['dish_type']}
    # ]
   #inlines = [Reviews]
   ordering = ['reviews']

admin.site.register(Menu, MenuAdmin)
admin.site.register(FoodType, FoodTypeAdmin)

