from django.urls import path

from . import studentViews

urlpatterns = [
    path('login/', studentViews.login, name="Login"), #done for intern
    path('profile/', studentViews.studentProfile, name="Student Profile"), #done for intern
    path('getDashboard/', studentViews.getDashboard, name="Dashboard"), # customised dashboard..  check are we checking registedred  check allowed branch/batches filter in
    path("addResume/", studentViews.addResume, name="Upload Resume"), #done for intern
    path("deleteResume/", studentViews.deleteResume, name="Upload Resume"),#done for intern
    path("submitApplication/", studentViews.submitApplication, name="Submit Application"), #done for intern
    path("deleteApplication/", studentViews.deleteApplication, name="Delete Application"), #done for intern check for opening type data in headers
    path("getContributorStats/", studentViews.getContributorStats, name="Get Contributor Stats"),
    path("studentAcceptOffer/", studentViews.studentAcceptOffer, name="Student Accept Offer"), #same as above  check header
]
#store all files..