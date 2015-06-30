from django.contrib import admin
from menu.models import Menu, FoodItem, FoodType, Review  # , organizedMenu

# Register Models are will be edited in the Admin screen
# This may not include all models

class FoodTypeAdmin(admin.ModelAdmin):
    # list_display = ('FType')
    ordering = ['type']

class FoodAdmin(admin.StackedInline):
      model = FoodItem
      extra = 0

class ReviewAdmin(admin.ModelAdmin):
     ordering = ['id','foodItemName']

class MenuAdmin(admin.ModelAdmin):
    ordering = ['title']
    fieldsets = [
        (None, {'fields':['title']}),
        (None, {'fields':['logo']}),
    ]
    inlines = [FoodAdmin]

admin.site.register(Review,ReviewAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(FoodType, FoodTypeAdmin)


