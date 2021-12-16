from django.contrib import admin
from .models import *
from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.shortcuts import resolve_url
from django.utils.html import format_html
from django.utils.safestring import SafeText
from .models import *

admin.site.register(User)
admin.site.register(Admin)
admin.site.register(PrePlacementOffer)

admin.site.site_header = "CDC Recruitment Portal"


def model_admin_url(obj, name=None) -> str:
    url = resolve_url(admin_urlname(obj._meta, SafeText("change")), obj.pk)
    return format_html('<a href="{}">{}</a>', url, name or str(obj))


@admin.register(Student)
class Student(admin.ModelAdmin):
    list_display = ("roll_no", "name", "batch", "branch", "phone_number")
    search_fields = ("roll_no", "name","phone_number")
    ordering = ("roll_no", "name", "batch", "branch", "phone_number")
    list_filter = ("batch", "branch")


@admin.register(Placement)
class Placement(admin.ModelAdmin):
    list_display = (COMPANY_NAME, CONTACT_PERSON_NAME, PHONE_NUMBER, 'tier', 'compensation_CTC')
    search_fields = (COMPANY_NAME, CONTACT_PERSON_NAME)
    ordering = (COMPANY_NAME, CONTACT_PERSON_NAME, 'tier', 'compensation_CTC')
    list_filter = ('tier',)


@admin.register(PlacementApplication)
class PlacementApplication(admin.ModelAdmin):
    list_display = ('id', 'Placement', 'Student', 'selected')
    search_fields = ('id',)
    ordering = ('id',)
    list_filter = ('selected',)

    def Placement(self, obj):
        return model_admin_url(obj.placement)

    def Student(self, obj):
        return model_admin_url(obj.student)


