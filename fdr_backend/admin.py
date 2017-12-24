from django.contrib import admin
from django.contrib.staticfiles.templatetags.staticfiles import static
# Register your models here.

from .models import  FaceEntry, Face
from django.templatetags.static import static
from django.conf import settings
from django.utils.html import format_html

class FaceAdmin(admin.ModelAdmin):
    def get_photo(self, obj):
        return format_html('<img src="%s" />' % ('http://' + settings.STATIC_ROOT + static(obj.image)))
    get_photo.allow_tags = True
    list_display = ('uuid', 'get_photo', 'timestamp')

class FaceEntryAdmin(admin.ModelAdmin):
    def get_photo(self, obj):
        return format_html('<img src="%s" />' % ('http://' + settings.STATIC_ROOT + static(obj.image)))

    get_photo.allow_tags = True
    list_display = ('face', 'get_photo', 'timestamp')


admin.site.register(FaceEntry, FaceEntryAdmin)
admin.site.register(Face, FaceAdmin)
