import json
from django.http import Http404
from django.views.generic import ListView, View, DetailView, UpdateView, FormView
from django.shortcuts import render, reverse, redirect
from django.core.paginator import Paginator
from . import models, forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from users import mixins as user_mixins
from django.db.models import Count, F, Func
import math
import random

# Create your views here.


class SalonSearchView(View):
    """SearchView Definition"""

    def get(self, request):
        form = forms.SalonSearchForm(request.GET)
        if form.is_valid():
            search_data = form.cleaned_data.get("salon_search")
            if len(search_data) != 0:
                filter_args1 = {}
                filter_args2 = {}
                filter_args1["name__contains"] = search_data
                filter_args2["address__contains"] = search_data
                qs1 = (
                    models.Salon.objects.filter(**filter_args1)
                    .order_by(
                        "-created",
                    )
                )
                qs2 = (
                    models.Salon.objects.filter(**filter_args2)
                    .order_by(
                        "-created",
                    )
                )
                qs = qs1 | qs2

                paginator = Paginator(qs, 10)
                page = request.GET.get("page", 1)
                salons = paginator.get_page(page)
                if qs.count() > 0:
                    print("@@@@@@@@@@@")
                    return render(
                        request,
                        "salons/salon_search.html",
                        {"form": form, "salons": salons, "page_obj": salons,"page_sorted": "search"},
                    )
                elif qs.count() == 0:
                    form = forms.SalonSearchForm()
                    return render(
                        request,
                        "salons/salon_search.html",
                        {"form": form, "empty_search": "ok", "page_sorted": "search"},
                    )
        form = forms.SalonSearchForm()
        return render(
            request,
            "salons/salon_search.html",
            {"form": form, "empty_search": "ok", "page_sorted": "search"},
        )