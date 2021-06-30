import json
from django.views.generic import ListView, View, DetailView, UpdateView, FormView
from django.shortcuts import render, reverse, redirect
from django.core.paginator import Paginator
from . import models, forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from users import mixins as user_mixins

# Create your views here.


class HomeView(ListView):
    """StudioView Definition"""

    model = models.Studio
    paginate_by = 2
    ordering = "created"
    context_object_name = "studios"
    template_name = "studios/studio_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.user)
        temp = {}
        if self.request.user.is_authenticated:  # 로그인 되면 실행됨 # 로그인 X 시 스킵
            aa = models.Studio.objects.filter(likes_user=self.request.user).values_list(
                "pk", flat=True
            )
            print(aa)
            context["check_exist"] = aa
        else:
            context["check_exist"] = temp
        return context


# HomeView--> main_list로 대체`
# 사유 : 로그인 했는지 안했는지의 차이를 두기 위해
# 2021-06-30  다시 HomeView 사용
# 사유 : 페이지네이션 사용편이


def main_list(request):
    studios = models.Studio.objects.filter()
    temp = {}
    if request.user.is_authenticated:  # 로그인 되면 실행됨 # 로그인 X 시 스킵
        check_exist = models.Studio.objects.filter(likes_user=request.user).values_list(
            "pk",
            flat=True,
        )

        return render(
            request,
            "studios/studio_list.html",
            {"studios": studios, "check_exist": check_exist},
        )
    return render(
        request,
        "studios/studio_list.html",
        {
            "studios": studios,
            "check_exist": temp,
        },
    )


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


class StudioProfileView(DetailView):
    model = models.Studio
    template_name = "studios/studio_profile.html"


class EditStudioView(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.Studio
    template_name = "studios/studio_edit.html"
    fields = (
        "name",
        "studio_avatar",
        "studio_best_photo",
        "phone_number",
        "kakao_chat",
        "address",
        "open_time",
        "close_time",
        "introduction",
        "using_info",
    )

    def get_object(self, queryset=None):  # 룸 호스트랑 요청하는 사람이랑 같은지
        studio = super().get_object(queryset=queryset)
        if studio.author.pk != self.request.user.pk:
            return reverse("core:home")
        return studio

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["phone_number"].widget.attrs = {"placeholder": "- 제외"}
        form.fields["open_time"].widget.attrs = {"placeholder": "10:00"}
        form.fields["close_time"].widget.attrs = {"placeholder": "20:00"}

        form.fields["name"].label = "사진관 이름"
        form.fields["studio_avatar"].label = "사진관 프로필 사진"
        form.fields["studio_best_photo"].label = "작가님의 베스트 사진"
        form.fields["address"].label = "사진관 주소"
        form.fields["phone_number"].label = "전화번호"
        form.fields["kakao_chat"].label = "카카오톡 오픈채팅 주소"
        form.fields["open_time"].label = "오픈 시간"
        form.fields["close_time"].label = "마감 시간"
        form.fields["introduction"].label = "사진관 소개"
        form.fields["using_info"].label = "사진관 이용안내"
        return form


class CreateStudioView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreateStudioForm
    template_name = "studios/studio_create.html"

    def form_valid(self, form):
        studio = form.save()
        studio.author = self.request.user
        studio.save()
        return redirect(reverse("studios:profile", kwargs={"pk": studio.pk}))
