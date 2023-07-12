from django.urls import path

from . import companyViews

urlpatterns = [
    path('addInternship/', companyViews.addInternship, name="Add Internship"),
]
