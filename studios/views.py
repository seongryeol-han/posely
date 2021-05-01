from django.views.generic import ListView, View
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models, forms

# Create your views here.


class HomeView(ListView):
    """StudioView Definition"""

    model = models.Studio
    paginate_by = 10
    ordering = "created"
    context_object_name = "studios"


class SearchView(View):
    """SearchView Definition"""

    def get(self, request):

        name = request.GET.get("name")
        address = request.GET.get("address")

        if bool(name) or bool(address):

            form = forms.SearchForm(request.GET)

            if form.is_valid():
                name = form.cleaned_data.get("name")
                address = form.cleaned_data.get("address")
                filter_args = {}

                if name is not None:
                    filter_args["name__startswith"] = name

                if address is not None:
                    filter_args["address__contains"] = address

                qs = models.Studio.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                studios = paginator.get_page(page)
                return render(
                    request, "studios/search.html", {"form": form, "studios": studios}
                )

        else:
            form = forms.SearchForm()
            return render(request, "studios/search.html", {"form": form})
