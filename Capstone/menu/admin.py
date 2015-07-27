"""
Built-in, globally-available admin actions.
From contrib/admin/actions.py
"""
from django.contrib import messages
from django.contrib.admin import helpers
from django.contrib.admin.utils import get_deleted_objects, model_ngettext
from django.core.exceptions import PermissionDenied
from django.db import router
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _, ugettext_lazy


def delete_selected(modeladmin, request, queryset):
    """
    Default action which deletes the selected objects.

    This action first displays a confirmation page whichs shows all the
    deleteable objects, or, if the user has no permission one of the related
    childs (foreignkeys), a "permission denied" message.

    Next, it deletes all selected objects and redirects back to the change list.
    """
    opts = modeladmin.model._meta
    app_label = opts.app_label

    # Check that the user has delete permission for the actual model
    if not modeladmin.has_delete_permission(request):
        raise PermissionDenied

    using = router.db_for_write(modeladmin.model)

    # Populate deletable_objects, a data structure of all related objects that
    # will also be deleted.
    deletable_objects, model_count, perms_needed, protected = get_deleted_objects(
        queryset, opts, request.user, modeladmin.admin_site, using)

    # The user has already confirmed the deletion.
    # Do the deletion and return a None to display the change list view again.
    if request.POST.get('post'):
        if perms_needed:
            raise PermissionDenied
        n = queryset.count()
        if n:
            for obj in queryset:
                obj_display = force_text(obj)
                modeladmin.log_deletion(request, obj, obj_display)
                obj.delete()
            #queryset.delete()
            modeladmin.message_user(request, _("Successfully deleted %(count)d %(items)s.") % {
                "count": n, "items": model_ngettext(modeladmin.opts, n)
            }, messages.SUCCESS)
        # Return None to display the change list page again.
        return None

    if len(queryset) == 1:
        objects_name = force_text(opts.verbose_name)
    else:
        objects_name = force_text(opts.verbose_name_plural)

    if perms_needed or protected:
        title = _("Cannot delete %(name)s") % {"name": objects_name}
    else:
        title = _("Are you sure?")

    context = dict(
        modeladmin.admin_site.each_context(request),
        title=title,
        objects_name=objects_name,
        deletable_objects=[deletable_objects],
        model_count=dict(model_count).items(),
        queryset=queryset,
        perms_lacking=perms_needed,
        protected=protected,
        opts=opts,
        action_checkbox_name=helpers.ACTION_CHECKBOX_NAME,
    )

    request.current_app = modeladmin.admin_site.name

    # Display the confirmation page
    return TemplateResponse(request, modeladmin.delete_selected_confirmation_template or [
        "admin/%s/%s/delete_selected_confirmation.html" % (app_label, opts.model_name),
        "admin/%s/delete_selected_confirmation.html" % app_label,
        "admin/delete_selected_confirmation.html"
    ], context)

delete_selected.short_description = ugettext_lazy("Delete selected %(verbose_name_plural)s")
"""
_________________________________________________________________________________________________
"""
# Register Models will be edited in the Admin screen
# This may not include all models
from django.contrib import admin
from menu.models import Menu, GID, FoodItem, FoodType, Review

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
        (None, {'fields':['thumbnail']}),
        (None, {'fields':['createdOn']}),
        (None, {'fields':['createdBy']}),
        (None, {'fields':['rating']}),
        (None, {'fields':['type']}),
        (None, {'fields':['isActive']})]
    extra = 0
    actions = [delete_selected]

class ReviewAdmin(admin.ModelAdmin):
    ordering = ['isActive']
    fieldsets = [
        (None, {'fields':['createdOn']}),
        (None, {'fields':['createdBy']}),
        (None, {'fields':['reviewComment']}),
        (None, {'fields':['rating']}),
        (None, {'fields':['logo']}),
        (None, {'fields':['isActive']})]
    extra = 0
    actions = [delete_selected]

class MenuAdmin(admin.ModelAdmin):
    list_display = ['menuName','id']
    list_filter = ['createdOn','createdBy']
    '''filter_horizontal= ('gid',) -Optional'''
    fieldsets = [
        (None, {'fields':['menuName']}),
        (None, {'fields':['logo']}),
        (None, {'fields':['thumbnail']}),
        (None, {'fields':['createdOn']}),
        (None, {'fields':['createdBy']}),
        (None, {'fields':['gid']}),
        (None, {'fields':['isActive']})]

    inlines = [FoodAdmin]
    actions = [delete_selected]

admin.site.register(Review,ReviewAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(FoodType, FoodTypeAdmin)
admin.site.register(GID,GIDAdmin)
