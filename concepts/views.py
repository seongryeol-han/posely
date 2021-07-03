from django.views.generic import DetailView, ListView, FormView
from django.shortcuts import render, redirect, reverse
from . import models, forms
from users import mixins as user_mixins

# Create your views here.


class ConceptDetail(DetailView):
    """ConceptDetail Definition"""

    model = models.Concept


class ConceptEditListView(ListView):

    """HomeView Definition"""

    template_name = "concepts/concept_edit.html"
    model = models.Concept
    ordering = "created"
    context_object_name = "concepts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
