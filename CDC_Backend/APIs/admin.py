from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Placement)
admin.site.register(PlacementApplication)
admin.site.register(PrePlacementOffer)
