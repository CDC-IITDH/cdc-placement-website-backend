from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.shortcuts import resolve_url
from django.utils.html import format_html
from django.utils.safestring import SafeText

from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportMixin, ExportMixin
from import_export import resources

from .models import *

class UserAdmin(ImportExportMixin, SimpleHistoryAdmin):
    pass

admin.site.register(User,UserAdmin)
admin.site.register(Admin, SimpleHistoryAdmin)

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
        exclude = ('id','changed_by', 'is_company_details_pdf', 'is_description_pdf',
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
