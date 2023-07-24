from django.urls import path, include

from . import companyUrls

urlpatterns = [
    path('company/', include(companyUrls)),
]
