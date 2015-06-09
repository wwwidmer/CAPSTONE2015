from django.contrib import admin
from menu.models import Menu, FoodItem

# Register Models are will be edited in the Admin screen
# This may not include all models

class MenuAdmin(admin.ModelAdmin):
    ordering = ["-id"]
class FoodAdmin(admin.ModelAdmin):
    list_display = ('dishname',id)
    ordering = ("-id",'dishname')

admin.site.register(Menu,MenuAdmin)
admin.site.register(FoodItem,FoodAdmin)