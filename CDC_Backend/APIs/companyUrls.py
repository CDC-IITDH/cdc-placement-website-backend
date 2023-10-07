from django.urls import path

from . import companyViews

urlpatterns = [
    path('addPlacement/', companyViews.addPlacement, name="Add Placement"),
    path('verifyEmail/', companyViews.verifyEmail, name="Verify Email"),
    path('getAutoFillJnf/', companyViews.autoFillJnf, name="Auto FIll JNF"),
    path('addInternship/',companyViews.addInternship,name="Add Internship"),
    path('getAutoFillInf/', companyViews.autoFillInf, name="Auto FIll INF"),
]
