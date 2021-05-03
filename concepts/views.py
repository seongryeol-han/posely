from django.views.generic import DetailView, ListView
from django.shortcuts import render
from django.urls import reverse
from . import models

# Create your views here.


def SelectConcept(request,pk):
    """SelectConcept Definition"""

    
    concept = models.Concept.objects.get(pk=pk)
    aa = concept.studio.name
    print(concept,aa)
    return render(request, "studios/detail.html", {})