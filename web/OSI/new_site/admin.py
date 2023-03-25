from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserRating)
admin.site.register(Report)
admin.site.register(WorkType)
admin.site.register(Stage)
admin.site.register(TimeFactor)