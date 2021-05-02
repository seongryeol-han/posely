from django.views.generic import DetailView, ListView
from django.shortcuts import render
from . import models

# Create your views here.


class SelectConcept(DetailView):
    """SelectConcept Definition"""

    model = models.Concept
