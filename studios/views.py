import json
from django.views.generic import ListView, View, DetailView
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models, forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Create your views here.


class HomeView(ListView):
    """StudioView Definition"""

    model = models.Studio
    paginate_by = 10
    ordering = "created"
    context_object_name = "studios"


# HomeView--> main_list로 대체
# 사유 : 로그인 했는지 안했는지의 차이를 두기 위해


def main_list(request):
    studios = models.Studio.objects.filter()

    if request.user.is_authenticated:  # 로그인 되면 실행됨 # 로그인 X 시 스킵
        check_exist = models.Studio.objects.filter(likes_user=request.user).values_list(
            "pk", flat=True
        )

        return render(
            request,
            "studios/studio_list.html",
            {"studios": studios, "check_exist": check_exist},
        )
    return render(request, "studios/studio_list.html", {"studios": studios})


class SelectStudio(DetailView):
    model = models.Studio
    pk_url_kwarg = "pk"


class SearchView(View):
    """SearchView Definition"""

    def get(self, request):

        form = forms.SearchForm(request.GET)

        if form.is_valid():

            search_data = form.cleaned_data.get("search_name_address")

            if len(search_data) != 0:
                filter_args1 = {}
                filter_args2 = {}

                filter_args1["name__startswith"] = search_data

                filter_args2["address__contains"] = search_data

                qs1 = models.Studio.objects.filter(**filter_args1).order_by("-created")
                qs2 = models.Studio.objects.filter(**filter_args2).order_by("-created")

                qs = qs1 | qs2

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                studios = paginator.get_page(page)
                return render(
                    request, "studios/search.html", {"form": form, "studios": studios}
                )

        form = forms.SearchForm()
        return render(request, "studios/search.html", {"form": form})


@login_required
@require_POST
def studio_like(request):
    print("@@@@@@@@@@@@")  # 통신하는지 않하는 체크하려고 두었습니다리
    pk = request.POST.get("pk", None)
    studio = get_object_or_404(models.Studio, pk=pk)
    user = request.user

    if studio.likes_user.filter(id=user.id).exists():
        studio.likes_user.remove(user)
        message = "좋아요 취소"

    else:
        studio.likes_user.add(user)
        message = "좋아요"
    context = {"likes_count": studio.count_likes_user(), "message": message}
    return HttpResponse(json.dumps(context), content_type="application/json")
