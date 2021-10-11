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

# sort by default


class HomeView(ListView):
    """StudioView Definition"""

    model = models.Studio
    paginate_by = 1
    ordering = "-created"
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
            context["check_exist"] = aa
        else:
            context["check_exist"] = temp
        context["page_sorted"] = "created"
        return context


# sort by like
class HomeView2(ListView):
    """StudioView Definition"""

    # model = models.Studio
    # model = models.Studio
    paginate_by = 1
    # print("#############################")
    # queryset = models.Studio.objects.annotate(like_count=Count("likes_user")).order_by(
    #     "-like_count",
    # )
    # print(queryset)
    # num_like = Count("likes_user")

    context_object_name = "studios"
    template_name = "studios/studio_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # test_idx가 세션있나 없나 체크
        if "test_idx" in self.request.session:
            del self.request.session["test_idx"]
            self.request.session["test_idx"] = random.randrange(1, 3)
        else:
            self.request.session["test_idx"] = random.randrange(1, 3)

        # print(self.request.user)
        temp = {}
        if self.request.user.is_authenticated:  # 로그인 되면 실행됨 # 로그인 X 시 스킵
            aa = models.Studio.objects.filter(likes_user=self.request.user).values_list(
                "pk", flat=True
            )

            context["check_exist"] = aa
        else:
            context["check_exist"] = temp
        context["page_sorted"] = "like"
        return context

    def get_queryset(self):
        ps_with_avg = (
            models.Studio.objects.annotate(like_count=Count("likes_user"))
            .order_by("-like_count")
            .distinct()
        )
        return ps_with_avg


class Sin(Func):
    function = "SIN"


class Cos(Func):
    function = "COS"


class Acos(Func):
    function = "ACOS"


class Radians(Func):
    function = "RADIANS"


# sort by distance
class HomeView3(ListView):
    """StudioView Definition"""

    model = models.Studio
    paginate_by = 10
    context_object_name = "studios"
    template_name = "studios/studio_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        print("sort by distance_get_context_data_part")
        print(self.request.user)
        temp = {}
        if self.request.user.is_authenticated:  # 로그인 되면 실행됨 # 로그인 X 시 스킵
            aa = models.Studio.objects.filter(likes_user=self.request.user).values_list(
                "pk", flat=True
            )
            context["check_exist"] = aa
        else:
            context["check_exist"] = temp
        context["page_sorted"] = "distance"
        return context

    def get_queryset(self):
        if self.request.GET.get("lat"):
            now_lat = float(self.request.GET.get("lat"))
            now_lng = float(self.request.GET.get("lng"))

            self.request.session["lat"] = now_lat
            self.request.session["lng"] = now_lng

        lng1 = self.request.session.get("lng")
        lat1 = self.request.session.get("lat")
        radlat = Radians(lat1)  # given latitude
        radlong = Radians(lng1)  # given longitude
        radflat = Radians(F("studio_lat"))
        radflong = Radians(F("studio_lng"))
        Expression = 3959.0 * Acos(
            Cos(radlat) * Cos(radflat) * Cos(radflong - radlong)
            + Sin(radlat) * Sin(radflat)
        )
        ps_with_avg = models.Studio.objects.annotate(distance=Expression).order_by(
            "distance"
        )
        return ps_with_avg


class HomeView4(ListView):
    """StudioView Definition"""

    model = models.Studio
    paginate_by = 7
    context_object_name = "studios"
    template_name = "studios/photo_studio_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        print("sort by distance_get_context_data_part")
        print(self.request.user)
        temp = {}
        if self.request.user.is_authenticated:  # 로그인 되면 실행됨 # 로그인 X 시 스킵
            aa = models.Studio.objects.filter(likes_user=self.request.user).values_list(
                "pk", flat=True
            )
            context["check_exist"] = aa
        else:
            context["check_exist"] = temp
        context["page_sorted"] = "distance"
        return context

    def get_queryset(self):
        if self.request.GET.get("lat"):
            now_lat = float(self.request.GET.get("lat"))
            now_lng = float(self.request.GET.get("lng"))

            self.request.session["lat"] = now_lat
            self.request.session["lng"] = now_lng

        lng1 = self.request.session.get("lng")
        lat1 = self.request.session.get("lat")
        radlat = Radians(lat1)  # given latitude
        radlong = Radians(lng1)  # given longitude
        radflat = Radians(F("studio_lat"))
        radflong = Radians(F("studio_lng"))
        Expression = 3959.0 * Acos(
            Cos(radlat) * Cos(radflat) * Cos(radflong - radlong)
            + Sin(radlat) * Sin(radflat)
        )
        ps_with_avg = models.Studio.objects.annotate(distance=Expression).order_by(
            "distance"
        )
        return ps_with_avg


# HomeView--> main_list로 대체`
# 사유 : 로그인 했는지 안했는지의 차이를 두기 위해
# 2021-06-30  다시 HomeView 사용
# 사유 : 페이지네이션 사용편이

# def main_list(request):
#     studios = models.Studio.objects.filter()
#     temp = {}
#     if request.user.is_authenticated:  # 로그인 되면 실행됨 # 로그인 X 시 스킵
#         check_exist = models.Studio.objects.filter(likes_user=request.user).values_list(
#             "pk",
#             flat=True,
#         )

#         return render(
#             request,
#             "studios/studio_list.html",
#             {"studios": studios, "check_exist": check_exist},
#         )
#     return render(
#         request,
#         "studios/studio_list.html",
#         {
#             "studios": studios,
#             "check_exist": temp,
#         },
#     )

class SearchView(View):
    """SearchView Definition"""

    def get(self, request):
        form = forms.SearchForm(request.GET)
        if form.is_valid():
            search_data = form.cleaned_data.get("search_name_address")
            if len(search_data) != 0:
                filter_args1 = {}
                filter_args2 = {}
                filter_args1["name__contains"] = search_data
                filter_args2["address__contains"] = search_data
                qs1 = (
                    models.Studio.objects.filter(**filter_args1)
                    .annotate(like_count=Count("likes_user"))
                    .order_by(
                        "-like_count",
                    )
                )
                qs2 = (
                    models.Studio.objects.filter(**filter_args2)
                    .annotate(like_count=Count("likes_user"))
                    .order_by(
                        "-like_count",
                    )
                )
                qs = qs1 | qs2

                paginator = Paginator(qs, 10, orphans=5)
                page = request.GET.get("page", 1)
                studios = paginator.get_page(page)
                if qs.count() > 0:
                    return render(
                        request,
                        "studios/search.html",
                        {"form": form, "studios": studios, "page_sorted": "search"},
                    )
                elif qs.count() == 0:
                    form = forms.SearchForm()
                    return render(
                        request,
                        "studios/search.html",
                        {"form": form, "empty_search": "ok", "page_sorted": "search"},
                    )
        form = forms.SearchForm()
        return render(
            request,
            "studios/search.html",
            {"form": form, "empty_search": "ok", "page_sorted": "search"},
        )


@login_required
@require_POST
def studio_like(request):
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
            raise Http404
        return studio

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["phone_number"].widget.attrs = {"placeholder": "- 를 포함해주세요."}
        form.fields["open_time"].widget.attrs = {"placeholder": "10:00"}
        form.fields["close_time"].widget.attrs = {"placeholder": "20:00"}
        form.fields["address"].widget.attrs = {"readonly": True}
        form.fields["kakao_chat"].widget.attrs = {
            "placeholder": "오픈 채팅방 주소(URL)를 등록해주세요."
        }

        form.fields["name"].label = "사진관 이름"
        form.fields["studio_avatar"].label = "사진관 프로필 사진"
        form.fields["address"].label = "사진관 주소"
        form.fields["phone_number"].label = "전화번호"
        form.fields["kakao_chat"].label = "카카오톡 오픈채팅 주소"
        form.fields["open_time"].label = "오픈 시간"
        form.fields["close_time"].label = "마감 시간"
        form.fields["introduction"].label = "사진관 소개"
        form.fields["using_info"].label = "사진관 이용안내"
        return form


# 아직 이미지,경도,위도, 안받아옵니다.(model image, blank=True 처리함 )
class CreateStudioView2(View):
    def post(self, request):
        print("여기는 포스트")

        name = request.POST["name"]
        studio_avatar = request.FILES["studio_avatar"]
        zonecode = request.POST["zonecode"]
        addr_short = request.POST["addr_short"]
        addr_detail = request.POST["addr_detail"]
        address = zonecode + " " + addr_short + " " + addr_detail
        phone_number = request.POST["phone_number"]
        kakao_chat = request.POST["kakao_chat"]
        open_time = request.POST["open_time"]
        close_time = request.POST["close_time"]
        introduction = request.POST["introduction"]
        using_info = request.POST["using_info"]
        studio_lat = request.POST["studio_lat"]
        studio_lng = request.POST["studio_lng"]

        studio = models.Studio.objects.create(
            name=name,
            addr_short=addr_short,
            addr_detail=addr_detail,
            address=address,
            phone_number=phone_number,
            kakao_chat=kakao_chat,
            open_time=open_time,
            close_time=close_time,
            introduction=introduction,
            using_info=using_info,
            author=request.user,
            studio_avatar=studio_avatar,
            studio_lat=studio_lat,
            studio_lng=studio_lng,
        )
        self.request.user.has_studio = studio
        self.request.user.save()
        pk = self.kwargs.get("pk")

        return redirect(reverse("studios:concept-create", kwargs={"pk": studio.pk}))

    def get(self, request):
        if request.user.is_authenticated:
            if self.request.user.studio is True:
                if self.request.user.has_studio is None:
                    # studio_form = forms.CreateStudioForm
                    return render(
                        request,
                        "studios/studio_create2.html",
                        # {"studio_form": studio_form},
                    )

        return render(
            request,
            "studios/error_.html",
        )


# 0708 블락 처리 : 사유 , 유연한 form 컨트롤
# class CreateStudioView(
#     user_mixins.LoggedInOnlyView, user_mixins.CreateStudioLimitView, FormView
# ):

#     form_class = forms.CreateStudioForm
#     template_name = "studios/studio_create.html"

#     def form_valid(self, form):

#         studio = form.save()
#         studio.author = self.request.user
#         studio.save()
#         self.request.user.has_studio = studio
#         self.request.user.save()
#         return redirect(reverse("studios:profile", kwargs={"pk": studio.pk}))

#     def get_form(self, form_class=None):
#         form = super().get_form(form_class=form_class)
#         form.fields["phone_number"].widget.attrs = {"placeholder": "- 제외"}
#         form.fields["open_time"].widget.attrs = {"placeholder": "10:00"}
#         form.fields["close_time"].widget.attrs = {"placeholder": "20:00"}

#         form.fields["name"].label = "사진관 이름"
#         form.fields["studio_avatar"].label = "사진관 프로필 사진"
#         form.fields["address"].label = "사진관 주소"
#         form.fields["phone_number"].label = "전화번호"
#         form.fields["kakao_chat"].label = "카카오톡 오픈채팅 주소"
#         form.fields["open_time"].label = "오픈 시간"
#         form.fields["close_time"].label = "마감 시간"
#         form.fields["introduction"].label = "사진관 소개"
#         form.fields["using_info"].label = "사진관 이용안내"
#         return form

#     # def get(self, request, *args, **kwargs):
#     #     if self.request.user.count_has_studio() is False:
#     #         return redirect("core:home")
#     #     return redirect(self.request, "studios/studio_create.html")


# def CreateStudioRenew(request,name,studio_avatar,phone_number,kakao_chat,
# address,open_time,close_time,introduction,using_info):
#     try:
#         if not request.user.is_authenticated :
#             raise LoginError()
#             if  request.user.count_has_studio()>=1:
#                 raise have_Sutdio_Error()
#         #
#     except(have_Sutdio_Error,LoginError):
#         return redirect(reverse("core:home"))


# 여기다가 둬야지 concept의 pk를 이용 가능
class CreateConceptView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreateConceptForm
    template_name = "concepts/concept_create.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        form.fields["name"].label = "컨셉 이름"
        form.fields["service_config"].label = "컨셉 이용안내"
        form.fields["price"].label = "가격"
        return form

    def form_valid(self, form):
        pk = self.kwargs.get("pk")  # form으로 pk를 갖다줘야해서 pk를 설정 (concept의 pk).
        concept = form.save(pk)  # pk를 줌
        return redirect(reverse("studios:concept_photos", kwargs={"pk": concept.pk}))


class ConceptSelectView(DetailView):

    model = models.Studio
    template_name = "concepts/concept_select.html"
    ordering = "created"


class StudioSearchView(View):
    """SearchView Definition"""

    def get(self, request):
        form = forms.StudioSearchForm(request.GET)
        if form.is_valid():
            search_data = form.cleaned_data.get("studio_search")
            if len(search_data) != 0:
                filter_args1 = {}
                filter_args2 = {}
                filter_args1["name__contains"] = search_data
                filter_args2["address__contains"] = search_data
                qs1 = (
                    models.Studio.objects.filter(**filter_args1)
                    .order_by(
                        "-created",
                    )
                )
                qs2 = (
                    models.Studio.objects.filter(**filter_args2)
                    .order_by(
                        "-created",
                    )
                )
                qs = qs1 | qs2

                paginator = Paginator(qs, 10)
                page = request.GET.get("page", 1)
                studios = paginator.get_page(page)
                if qs.count() > 0:
                    print("@@@@@@@@@@@")
                    return render(
                        request,
                        "studios/search2.html",
                        {"form": form, "studios": studios, "page_obj": studios,"page_sorted": "search"},
                    )
                elif qs.count() == 0:
                    form = forms.StudioSearchForm()
                    return render(
                        request,
                        "studios/search2.html",
                        {"form": form, "empty_search": "ok", "page_sorted": "search"},
                    )
        form = forms.StudioSearchForm()
        return render(
            request,
            "studios/search2.html",
            {"form": form, "empty_search": "ok", "page_sorted": "search"},
        )
