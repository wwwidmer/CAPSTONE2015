from django.contrib import admin
from menu.models import Menu, FoodItem, FoodType, Review  # , organizedMenu

# Register Models are will be edited in the Admin screen
# This may not include all models

class FoodTypeAdmin(admin.ModelAdmin):
    # list_display = ('FType')
    ordering = ['type']

class FoodAdmin(admin.StackedInline):
      model = FoodItem
      fieldsets = [
        (None, {'fields':['dishName']}),
        (None, {'fields':['type']}),
        (None, {'fields':['logo']}),
        (None, {'fields':['createdOn']}),
        (None, {'fields':['createdBy']}),
        (None, {'fields':['rating']}),
        (None, {'fields':['isActive']})]
      extra = 0

class ReviewAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['createdOn']}),
        (None, {'fields':['createdBy']}),
        (None, {'fields':['reviewComment']}),
        (None, {'fields':['rating']}),
        (None, {'fields':['logo']})]
    extra = 0
     #ordering = ['id','foodItemName']

class MenuAdmin(admin.ModelAdmin):
    ordering = ['id','menuName','gid']
    list_display = ['id','menuName','gid']
    fieldsets = [
        (None, {'fields':['menuName']}),
        (None, {'fields':['logo']}),
        (None, {'fields':['createdOn']}),
        (None, {'fields':['createdBy']}),
        (None, {'fields':['isActive']})]

    inlines = [FoodAdmin]

admin.site.register(Review,ReviewAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(FoodType, FoodTypeAdmin)