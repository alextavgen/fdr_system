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
    return render(request, 'fdr_backend/faceentry_list.html', {'filter': user_filter})
