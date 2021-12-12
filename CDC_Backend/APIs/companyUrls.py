from django.urls import path
from . import companyViews


urlpatterns = [
    path('addPlacement/', companyViews.addPlacement, name="Add Placement"),
]
