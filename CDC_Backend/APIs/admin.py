from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.shortcuts import resolve_url
from django.utils.html import format_html
from django.utils.safestring import SafeText

from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportMixin, ExportMixin
from import_export import resources

from .models import *


class ArrayFieldListFilter(admin.SimpleListFilter):
    """This is a list filter based on the values
    from a model's `keywords` ArrayField. """

    title = 'Roles'
    parameter_name = 'user_type'

    def lookups(self, request, model_admin):
        # Very similar to our code above, but this method must return a
        # list of tuples: (lookup_value, human-readable value). These
        # appear in the admin's right sidebar

        keywords = User.objects.values_list("user_type", flat=True)
        keywords = [(kw, kw) for sublist in keywords for kw in sublist if kw]
        keywords = sorted(set(keywords))
        return keywords

    def queryset(self, request, queryset):
        # when a user clicks on a filter, this method gets called. The
        # provided queryset with be a queryset of Items, so we need to
        # filter that based on the clicked keyword.

        lookup_value = self.value()  # The clicked keyword. It can be None!
        if lookup_value:
            # the __contains lookup expects a list, so...
            queryset = queryset.filter(user_type__contains=[lookup_value])
        return queryset


class UserAdmin(ImportExportMixin, SimpleHistoryAdmin):
    list_display = ('email', 'user_type', 'last_login_time')
    list_filter = (ArrayFieldListFilter, 'last_login_time')
    search_fields = ('email', 'user_type')
    ordering = ('email', 'user_type')


admin.site.register(User, UserAdmin)

admin.site.site_header = "CDC Recruitment Portal"


def model_admin_url(obj, name=None) -> str:
    url = resolve_url(admin_urlname(obj._meta, SafeText("change")), obj.pk)
    return format_html('<a href="{}">{}</a>', url, name or str(obj))


class StudentAdmin(ImportExportMixin, SimpleHistoryAdmin):
    pass


@admin.register(Student)
class Student(StudentAdmin):
    list_display = ("roll_no", "name", "batch", "branch", "phone_number", 'can_apply')
    search_fields = ("roll_no", "name", "phone_number")
    ordering = ("roll_no", "name", "batch", "branch", "phone_number")
    list_filter = ("batch", "branch")
    actions = ['mark_can_apply_as_no', 'mark_can_apply_as_yes']

    @admin.action(description="Deregister students")
    def mark_can_apply_as_no(self, request, queryset):
        queryset.update(can_apply=False)
        self.message_user(request, "Deregistered the users")

    @admin.action(description="Register students")
    def mark_can_apply_as_yes(self, request, queryset):
        queryset.update(can_apply=True)
        self.message_user(request, "Registered the users")


class PlacementResources(resources.ModelResource):
    class Meta:
        model = Placement
        exclude = ('id', 'changed_by', 'is_company_details_pdf', 'is_description_pdf',
                   'is_compensation_details_pdf', 'is_selection_procedure_details_pdf')


class AdminAdmin(ExportMixin, SimpleHistoryAdmin):
    resource_class = PlacementResources


@admin.register(Placement)
class Placement(AdminAdmin):
    list_display = (COMPANY_NAME, CONTACT_PERSON_NAME, PHONE_NUMBER, 'tier', 'compensation_CTC')
    search_fields = (COMPANY_NAME, CONTACT_PERSON_NAME)
    ordering = (COMPANY_NAME, CONTACT_PERSON_NAME, 'tier', 'compensation_CTC')
    list_filter = ('tier',)


class PlacementApplicationResources(resources.ModelResource):
    class Meta:
        model = PlacementApplication
        exclude = ('id', 'changed_by')


class PlacementAdmin(ExportMixin, SimpleHistoryAdmin):
    resource_class = PlacementApplicationResources


@admin.register(PlacementApplication)
class PlacementApplication(PlacementAdmin):
    list_display = ('id', 'Placement', 'Student', 'selected')
    search_fields = ('id',)
    ordering = ('id',)
    list_filter = ('selected',)

    def Placement(self, obj):
        return model_admin_url(obj.placement)

    def Student(self, obj):
        return model_admin_url(obj.student)


class PrePlacementResources(resources.ModelResource):
    class Meta:
        model = PrePlacementOffer
        exclude = ('id', 'changed_by')


class PrePlacementOfferAdmin(ExportMixin, SimpleHistoryAdmin):
    resource_class = PrePlacementResources


@admin.register(PrePlacementOffer)
class PrePlacementOffer(PrePlacementOfferAdmin):
    list_display = ('company', 'Student', 'accepted')
    search_fields = ('company',)
    ordering = ('company',)
    list_filter = ('accepted',)

    def Student(self, obj):
        return model_admin_url(obj.student)
