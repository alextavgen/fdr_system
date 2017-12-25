from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic import ListView
from .models import  FaceEntry, Face, FaceEntryFilter


class FaceList(ListView):
    model = Face

class FaceEntryList(ListView):
    model = FaceEntry


def search(request):
    user_list = FaceEntry.objects.all()
    user_filter = FaceEntryFilter(request.GET, queryset=user_list)
    distinct_list = user_list.values('face').distinct().count()
    print(distinct_list)
    #distinct = FaceEntryFilter(request.GET, queryset=distinct_list)
    return render(request, 'fdr_backend/faceentry_list.html', {'filter': user_filter, 'distinct': distinct_list})
