from django.urls import path
from .views import FaceList, FaceEntryList, search


urlpatterns = [
    path('faces/', FaceList.as_view(), name='face_list'),
#    path('face_entries/', FaceEntryList.as_view(), name='faceentry_list'),
    path('face_entries/', search, name='faceentry_list'),
]
