from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic import ListView
from .models import  FaceEntry, Face, FaceEntryFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import plotly.offline as opy
import plotly.graph_objs as go

class FaceList(ListView):
    model = Face

class FaceEntryList(ListView):
    model = FaceEntry


def search(request):
    user_list = FaceEntry.objects.all()

    user_filter = FaceEntryFilter(request.GET, queryset=user_list)
    distinct_list = user_list.values('face').distinct().count()

    paginator = Paginator(user_filter.qs, 25)
    page = request.GET.get('page')
    entries = paginator.get_page(page)
    #grouped = user_list.order_by('face').distinct().count()
    #print(user_list)
    #https://stackoverflow.com/questions/36846395/embedding-a-plotly-chart-in-a-django-template
    #distinct = FaceEntryFilter(request.GET, queryset=distinct_list)
    return render(request, 'fdr_backend/faceentry_list.html', {'filter': user_filter, 'distinct': distinct_list, 'entries':entries})
