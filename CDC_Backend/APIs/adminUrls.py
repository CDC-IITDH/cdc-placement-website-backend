from django.urls import path

from . import adminViews

urlpatterns = [
    path('markStatus/', adminViews.markStatus, name="Mark Status"),
    path('getDashboard/', adminViews.getDashboard, name="Get Dashboard"),
    path('updateDeadline/', adminViews.updateDeadline, name="Update Deadline"),
    path('updateOfferAccepted/', adminViews.updateOfferAccepted, name="Update Offer Accepted"),
    path('updateEmailVerified', adminViews.updateEmailVerified, name="Update Email Verified"),
    path('deleteAdditionalInfo/', adminViews.deleteAdditionalInfo, name="Delete Additional Info"),
    path('addAdditionalInfo/', adminViews.addAdditionalInfo, name="Add Additional Info"),
    path('getApplications/', adminViews.getApplications, name="Get Applications"),
    path("submitApplication/", adminViews.submitApplication, name="Submit Application"),
    path('generateCSV/', adminViews.generateCSV, name="Generate CSV"),
    path('addPPO/', adminViews.addPPO, name="Add PPO"),
    path('getStudentApplication/', adminViews.getStudentApplication, name="Get student application"),
    path('getStats/', adminViews.getStats, name="Get Stats"),
]
