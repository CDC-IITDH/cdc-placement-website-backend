from django.urls import path
from . import companyViews


urlpatterns = [
    path('addOpening/', companyViews.addOpening, name="Add Opening"),
]
