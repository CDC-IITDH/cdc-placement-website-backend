from django.urls import path
from . import adminViews


urlpatterns = [
    path('markStatus/', adminViews.markStatus, name="Mark Status"),

]
