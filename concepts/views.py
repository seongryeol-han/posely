from django.views.generic import DetailView
from django.shortcuts import render
from . import models

# Create your views here.


class ConceptDetail(DetailView):
    """ConceptDetail Definition"""

    model = models.Concept