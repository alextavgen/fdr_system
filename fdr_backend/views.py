from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic import ListView
from .models import  FaceEntry, Face


class FaceList(ListView):
    model = Face
