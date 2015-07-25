from django.contrib import admin
from menu.models import Menu, GID, FoodItem, FoodType, Review  # , organizedMenu
# Register Models will be edited in the Admin screen
# This may not include all models

class FoodTypeAdmin(admin.ModelAdmin):
    # list_display = ('FType')
    ordering = ['type']
class GIDAdmin(admin.ModelAdmin):
    ordering = ['gid']
class FoodAdmin(admin.StackedInline):
      model = FoodItem
      filter_horizontal= ('type',)
      fieldsets = [
        (None, {'fields':['dishName']}),
        (None, {'fields':['logo']}),
        (None, {'fields':['createdOn']}),
        (None, {'fields':['createdBy']}),
        (None, {'fields':['rating']}),
        (None, {'fields':['type']}),
        (None, {'fields':['isActive']})]
      extra = 0

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['createdOn','id','reviewComment']
    ordering = ['isActive']
    fieldsets = [
        (None, {'fields':['createdOn']}),
        (None, {'fields':['createdBy']}),
        (None, {'fields':['reviewComment']}),
        (None, {'fields':['rating']}),
        (None, {'fields':['logo']}),
        (None, {'fields':['isActive']})]
    extra = 0
        #ordering = ['id','foodItemName']

class MenuAdmin(admin.ModelAdmin):
    list_display = ['menuName','id']
    list_filter = ['createdOn','createdBy']
    #filter_horizontal= ('gid',) -Optional#
    fieldsets = [
        (None, {'fields':['menuName']}),
        (None, {'fields':['logo']}),
        (None, {'fields':['createdOn']}),
        (None, {'fields':['createdBy']}),
        (None, {'fields':['gid']}),
        (None, {'fields':['isActive']})]

    inlines = [FoodAdmin]

admin.site.register(Review,ReviewAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(FoodType, FoodTypeAdmin)
admin.site.register(GID,GIDAdmin)
