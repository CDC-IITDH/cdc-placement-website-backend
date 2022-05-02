from django.urls import path, include

from . import studentViews, studentUrls, companyUrls, adminUrls

urlpatterns = [
    path('login/', studentViews.login, name="Login"),
    path('student/', include(studentUrls)),
    path('company/', include(companyUrls)),
    path('admin/', include(adminUrls)),

]
