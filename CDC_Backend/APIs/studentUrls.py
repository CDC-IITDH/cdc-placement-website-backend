from django.urls import path

from . import studentViews

urlpatterns = [
    path('login/', studentViews.login, name="Login"),
    path('profile/', studentViews.studentProfile, name="Student Profile"),
    path('getDashboard/', studentViews.getDashboard, name="Dashboard"),
    path("addResume/", studentViews.addResume, name="Upload Resume"),
    path("deleteResume/", studentViews.deleteResume, name="Upload Resume"),
    path("submitApplication/", studentViews.submitApplication, name="Submit Application"),
    path("deleteApplication/", studentViews.deleteApplication, name="Delete Application"),
]
