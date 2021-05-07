from django.views.generic import ListView, View, DetailView
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


class SelectStudio(DetailView):
    model = models.Studio
    pk_url_kwarg = "pk"


class SearchView(View):
    """SearchView Definition"""

    def get(self, request):

        search_data = request.GET.get("search_name_address")

        form = forms.SearchForm(request.GET)

        if form.is_valid():
            filter_args1 = {}
            filter_args2 = {}

            filter_args1["name__startswith"] = search_data

            filter_args2["address__contains"] = search_data

            qs1 = models.Studio.objects.filter(**filter_args1).order_by("-created")
            qs2 = models.Studio.objects.filter(**filter_args2).order_by("-created")
            
            qs = qs1|qs2
            
            paginator = Paginator(qs, 10, orphans=5)

            page = request.GET.get("page", 1)
           
            studios = paginator.get_page(page)
            return render(
                request, "studios/search.html", {"form": form, "studios": studios}
            )

        else:
            form = forms.SearchForm()
            return render(request, "studios/search.html", {"form": form})
