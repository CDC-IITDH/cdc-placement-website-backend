from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.shortcuts import resolve_url
from django.utils.html import format_html
from django.utils.safestring import SafeText

from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportMixin

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


@admin.register(Placement)
class Placement(SimpleHistoryAdmin):
    list_display = (COMPANY_NAME, CONTACT_PERSON_NAME, PHONE_NUMBER, 'tier', 'compensation_CTC')
    search_fields = (COMPANY_NAME, CONTACT_PERSON_NAME)
    ordering = (COMPANY_NAME, CONTACT_PERSON_NAME, 'tier', 'compensation_CTC')
    list_filter = ('tier',)


@admin.register(PlacementApplication)
class PlacementApplication(SimpleHistoryAdmin):
    list_display = ('id', 'Placement', 'Student', 'selected')
    search_fields = ('id',)
    ordering = ('id',)
    list_filter = ('selected',)

    def Placement(self, obj):
        return model_admin_url(obj.placement)

    def Student(self, obj):
        return model_admin_url(obj.student)


@admin.register(PrePlacementOffer)
class PrePlacementOffer(SimpleHistoryAdmin):
    list_display = ('company', 'Student', 'accepted')
    search_fields = ('company',)
    ordering = ('company',)
    list_filter = ('accepted',)

    def Student(self, obj):
        return model_admin_url(obj.student)
