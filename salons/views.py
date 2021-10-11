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



class ConceptDetail(DetailView):
    """ConceptDetail Definition"""

    model = models.Concept


class SalonProfileView(DetailView):
    model = models.Salon
    template_name = "salons/salon_profile.html"



class EditSalonView(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.Salon
    template_name = "salons/salon_edit.html"
    fields = (
        "name",
        "salon_avatar",
        "phone_number",
        "kakao_chat",
        "address",
        "open_time",
        "close_time",
        "introduction",
        "using_info",
    )

    def get_object(self, queryset=None):  # 룸 호스트랑 요청하는 사람이랑 같은지
        salon = super().get_object(queryset=queryset)
        if salon.stylist.pk != self.request.user.pk:
            raise Http404
        return salon

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["phone_number"].widget.attrs = {"placeholder": "- 를 포함해주세요."}
        form.fields["open_time"].widget.attrs = {"placeholder": "10:00"}
        form.fields["close_time"].widget.attrs = {"placeholder": "20:00"}
        form.fields["address"].widget.attrs = {"readonly": True}
        form.fields["kakao_chat"].widget.attrs = {
            "placeholder": "오픈 채팅방 주소(URL)를 등록해주세요."
        }

        form.fields["name"].label = "미용실 이름"
        form.fields["salon_avatar"].label = "미용실 프로필 사진"
        form.fields["address"].label = "미용실 주소"
        form.fields["phone_number"].label = "전화번호"
        form.fields["kakao_chat"].label = "카카오톡 오픈채팅 주소"
        form.fields["open_time"].label = "오픈 시간"
        form.fields["close_time"].label = "마감 시간"
        form.fields["introduction"].label = "미용실 소개"
        form.fields["using_info"].label = "미용실 이용안내"
        return form


class ConceptEditListView(ListView):

    """HomeView Definition"""

    template_name = "salons/concept_edit-list.html"
    model = models.Concept
    ordering = "created"
    context_object_name = "concepts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CreateConceptView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreateConceptForm
    template_name = "salons/concept_create.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        form.fields["name"].label = "컨셉 이름"
        form.fields["service_config"].label = "컨셉 이용안내"
        form.fields["price"].label = "가격"
        return form

    def form_valid(self, form):
        pk = self.kwargs.get("pk")  # form으로 pk를 갖다줘야해서 pk를 설정 (concept의 pk).
        concept = form.save(pk)  # pk를 줌
        return redirect(reverse("salons:concept_photos", kwargs={"pk": concept.pk}))


class EditConceptView(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.Concept
    template_name = "salons/concept_edit.html"
    fields = (
        "name",
        "service_config",
        "price",
    )

    def form_valid(self, form):
        pk = self.kwargs.get("pk")  # form으로 pk를 갖다줘야해서 pk를 설정 (concept의 pk).
        form.save(pk)  # pk를 줌 form에다가
        return redirect(reverse("salons:concept_edit-list"))

    def get_object(self, queryset=None):
        concept = super().get_object(queryset=queryset)
        if concept.salon.stylist.pk != self.request.user.pk:
            raise Http404()
        return concept

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        form.fields["name"].label = "컨셉 이름"
        form.fields["service_config"].label = "컨셉 이용안내"
        form.fields["price"].label = "가격"
        return form


class ConceptPhotosView(user_mixins.LoggedInOnlyView, DetailView):
    model = models.Concept
    template_name = "salons/concept_photos.html"

    def get_object(self, queryset=None):  # 룸 호스트랑 요청하는 사람이랑 같은지
        concept = super().get_object(queryset=queryset)
        if concept.salon.stylist.pk != self.request.user.pk:
            raise Http404()
        return concept


@login_required  # 만약 로그인이 안되어 있으면, setting에서 LOGIN_URL 로 이동한다 (이거 설정해둬야함.)
def delete_photo(request, concept_pk, photo_pk):  # url.py에 등록되어있는거.
    user = request.user
    try:
        concept = models.Concept.objects.get(pk=concept_pk)
        if concept.salon.stylist.pk != user.pk:
            Http404()
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
        return redirect(reverse("salons:concept_photos", kwargs={"pk": concept_pk}))
    except models.Concept.DoesNotExist:  # concept이 없음
        return redirect(reverse("core:photo_home"))


@login_required  # 만약 로그인이 안되어 있으면, setting에서 LOGIN_URL 로 이동한다 (이거 설정해둬야함.)
def delete_concept(request, concept_pk):  # url.py에 등록되어있는거.
    user = request.user
    try:
        concept = models.Concept.objects.get(pk=concept_pk)
        if concept.salon.stylist.pk != user.pk:
            Http404()
        else:
            models.Concept.objects.filter(pk=concept_pk).delete()
        return redirect(reverse("salons:concept_edit-list"))
    except models.Concept.salon.DoesNotExist:  # concept이 없음
        return redirect(reverse("core:photo_home"))


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):

    model = models.Photo
    template_name = "salons/photo_create.html"
    fields = "file"
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")  # form으로 pk를 갖다줘야해서 pk를 설정 (concept의 pk).
        form.save(pk)  # pk를 줌 form에다가
        return redirect(reverse("salons:concept_photos", kwargs={"pk": pk}))