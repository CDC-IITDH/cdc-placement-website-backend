from django.urls import path

from . import studentViews

urlpatterns = [
    path('login/', studentViews.login, name="Login"), 
    path('profile/', studentViews.studentProfile, name="Student Profile"), 
    path('getDashboard/', studentViews.getDashboard, name="Dashboard"),
    path("addResume/", studentViews.addResume, name="Upload Resume"), 
    path("deleteResume/", studentViews.deleteResume, name="Delete Resume"),
    path("submitApplication/", studentViews.submitApplication, name="Add Application"), 
    path("deleteApplication/", studentViews.deleteApplication, name="Delete Application"), 
    path("getContributorStats/", studentViews.getContributorStats, name="Get Contributor Stats"),
    path("studentAcceptOffer/", studentViews.studentAcceptOffer, name="Student Accept Offer"), 
    path("addIssue/",studentViews.addIssue,name= "Add Issue")
]
