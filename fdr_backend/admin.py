from django.contrib import admin

# Register your models here.

from .models import Event, FaceEntry

admin.site.register(Event)
admin.site.register(FaceEntry)
