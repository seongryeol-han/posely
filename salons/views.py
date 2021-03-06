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
import datetime, random
from django.db.models.functions import Substr

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

    def get_object(self, queryset=None):  # ??? ???????????? ???????????? ???????????? ?????????
        salon = super().get_object(queryset=queryset)
        if salon.stylist.pk != self.request.user.pk:
            raise Http404
        return salon

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["phone_number"].widget.attrs = {"placeholder": "- ??? ??????????????????."}
        form.fields["open_time"].widget.attrs = {"placeholder": "10:00"}
        form.fields["close_time"].widget.attrs = {"placeholder": "20:00"}
        form.fields["address"].widget.attrs = {"readonly": True}
        form.fields["kakao_chat"].widget.attrs = {
            "placeholder": "?????? ????????? ??????(URL)??? ??????????????????."
        }

        form.fields["name"].label = "????????? ??????"
        form.fields["salon_avatar"].label = "????????? ????????? ??????"
        form.fields["address"].label = "????????? ??????"
        form.fields["phone_number"].label = "????????????"
        form.fields["kakao_chat"].label = "???????????? ???????????? ??????"
        form.fields["open_time"].label = "?????? ??????"
        form.fields["close_time"].label = "?????? ??????"
        form.fields["introduction"].label = "????????? ??????"
        form.fields["using_info"].label = "????????? ????????????"
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

        form.fields["name"].label = "?????? ??????"
        form.fields["service_config"].label = "?????? ????????????"
        form.fields["price"].label = "??????"
        return form

    def form_valid(self, form):
        pk = self.kwargs.get("pk")  # form?????? pk??? ?????????????????? pk??? ?????? (concept??? pk).
        concept = form.save(pk)  # pk??? ???
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
        pk = self.kwargs.get("pk")  # form?????? pk??? ?????????????????? pk??? ?????? (concept??? pk).
        form.save(pk)  # pk??? ??? form?????????
        return redirect(reverse("salons:concept_edit-list"))

    def get_object(self, queryset=None):
        concept = super().get_object(queryset=queryset)
        if concept.salon.stylist.pk != self.request.user.pk:
            raise Http404()
        return concept

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        form.fields["name"].label = "?????? ??????"
        form.fields["service_config"].label = "?????? ????????????"
        form.fields["price"].label = "??????"
        return form


class ConceptPhotosView(user_mixins.LoggedInOnlyView, DetailView):
    model = models.Concept
    template_name = "salons/concept_photos.html"

    def get_object(self, queryset=None):  # ??? ???????????? ???????????? ???????????? ?????????
        concept = super().get_object(queryset=queryset)
        if concept.salon.stylist.pk != self.request.user.pk:
            raise Http404()
        return concept


@login_required  # ?????? ???????????? ????????? ?????????, setting?????? LOGIN_URL ??? ???????????? (?????? ??????????????????.)
def delete_photo(request, concept_pk, photo_pk):  # url.py??? ?????????????????????.
    user = request.user
    try:
        concept = models.Concept.objects.get(pk=concept_pk)
        if concept.salon.stylist.pk != user.pk:
            Http404()
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
        return redirect(reverse("salons:concept_photos", kwargs={"pk": concept_pk}))
    except models.Concept.DoesNotExist:  # concept??? ??????
        return redirect(reverse("core:studio_home"))


@login_required  # ?????? ???????????? ????????? ?????????, setting?????? LOGIN_URL ??? ???????????? (?????? ??????????????????.)
def delete_concept(request, concept_pk):  # url.py??? ?????????????????????.
    user = request.user
    try:
        concept = models.Concept.objects.get(pk=concept_pk)
        if concept.salon.stylist.pk != user.pk:
            Http404()
        else:
            models.Concept.objects.filter(pk=concept_pk).delete()
        return redirect(reverse("salons:concept_edit-list"))
    except models.Concept.salon.DoesNotExist:  # concept??? ??????
        return redirect(reverse("core:studio_home"))


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):

    model = models.Photo
    template_name = "salons/photo_create.html"
    fields = "file"
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")  # form?????? pk??? ?????????????????? pk??? ?????? (concept??? pk).
        form.save(pk)  # pk??? ??? form?????????
        return redirect(reverse("salons:concept_photos", kwargs={"pk": pk}))


class SalonHomeView(ListView):
    """SalonHomeView Definition"""

    model = models.Photo
    paginate_by = 10
    context_object_name = "photos"
    template_name = "salons/salon_photo_list.html"

    def get_context_data(self, **kwargs):
        # print(self.request.GET.get("page", 1))
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        now = datetime.datetime.now()
        nowTime = now.strftime("%M")
        if len(nowTime) == 1:
            nowTime = "0" + nowTime
        nowTime = nowTime[1:2]
        # print(nowTime)
        target_idx = int(nowTime)
        print(target_idx)
        print(type(target_idx))

        # test_idx??? ???????????? ?????? ??????
        if "test_idx" in self.request.session:
            if target_idx != self.request.session["test_idx"]:
                del self.request.session["test_idx"]
                self.request.session["test_idx"] = target_idx
        else:
            self.request.session["test_idx"] = target_idx  # 0~6

        sort_idx = self.request.session.get("test_idx")
        ps_with_avg = None
        if sort_idx == 1:
            print("sort_idx==1")
            ps_with_avg = models.Photo.objects.annotate(random_int_split=Substr("random_int",1)).order_by("random_int_split")
        if sort_idx == 2:
            print("sort_idx==2")
            ps_with_avg = models.Photo.objects.annotate(random_int_split=Substr("random_int",2)).order_by("random_int_split")
        if sort_idx == 3:
            print("sort_idx==3")
            ps_with_avg = models.Photo.objects.annotate(random_int_split=Substr("random_int",3)).order_by("random_int_split")
        if sort_idx == 4:
            print("sort_idx==4")
            ps_with_avg = models.Photo.objects.annotate(random_int_split=Substr("random_int",4)).order_by("random_int_split")
        if sort_idx == 5:
            print("sort_idx==5")
            ps_with_avg = models.Photo.objects.annotate(random_int_split=Substr("random_int",5)).order_by("random_int_split")
        if sort_idx == 6:
            print("sort_idx==6")
            ps_with_avg = models.Photo.objects.annotate(random_int_split=Substr("random_int",5)).order_by("-random_int_split")
        if sort_idx == 7:
            print("sort_idx==7")
            ps_with_avg = models.Photo.objects.annotate(random_int_split=Substr("random_int",4)).order_by("-random_int_split")
        if sort_idx == 8:
            print("sort_idx==8")
            ps_with_avg = models.Photo.objects.annotate(random_int_split=Substr("random_int",3)).order_by("-random_int_split")
        if sort_idx == 9:
            print("sort_idx==9")
            ps_with_avg = models.Photo.objects.annotate(random_int_split=Substr("random_int",2)).order_by("-random_int_split")
        if sort_idx == 0:
            print("sort_idx==0")
            ps_with_avg = models.Photo.objects.annotate(random_int_split=Substr("random_int",1)).order_by("-random_int_split")
        return ps_with_avg



class CreateSalonView(View):
    def post(self, request):
        print("????????? ?????????")

        name = request.POST["name"]
        salon_avatar = request.FILES["salon_avatar"]
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
        salon_lat = request.POST["salon_lat"]
        salon_lng = request.POST["salon_lng"]

        salon = models.Salon.objects.create(
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
            stylist=request.user,
            salon_avatar=salon_avatar,
            salon_lat=salon_lat,
            salon_lng=salon_lng,
        )
        self.request.user.has_salon = salon
        self.request.user.save()
        pk = self.kwargs.get("pk")

        return redirect(reverse("salons:concept-create", kwargs={"pk": salon.pk}))

    def get(self, request):
        if request.user.is_authenticated:
            if self.request.user.salon is True:
                if self.request.user.has_salon is None:
                    return render(
                        request,
                        "salons/salon_create.html",
                    )

        return render(
            request,
            "salons/error_.html",
        )


class Sin(Func):
    function = "SIN"


class Cos(Func):
    function = "COS"


class Acos(Func):
    function = "ACOS"


class Radians(Func):
    function = "RADIANS"

class SalonDistanceView(ListView):
    """SalonDistanceView Definition"""

    model = models.Salon
    paginate_by = 7
    context_object_name = "salons"
    template_name = "salons/salon_distance_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        print("sort by distance_get_context_data_part")
        print(self.request.user)
        temp = {}
        if self.request.user.is_authenticated:  # ????????? ?????? ????????? # ????????? X ??? ??????
            aa = models.Salon.objects.filter(likes_user=self.request.user).values_list(
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
        radflat = Radians(F("salon_lat"))
        radflong = Radians(F("salon_lng"))
        Expression = 3959.0 * Acos(
            Cos(radlat) * Cos(radflat) * Cos(radflong - radlong)
            + Sin(radlat) * Sin(radflat)
        )
        ps_with_avg = models.Salon.objects.annotate(distance=Expression).order_by(
            "distance"
        )
        return ps_with_avg


class SalonButtonFilterView(View):
    """SearchView Definition"""

    def get(self, request):
        form = forms.SalonPhotoFilterForm(request.GET)
        if form.is_valid():
            search_data = form.cleaned_data.get("salon_photo_filter")
            if len(search_data) != 0:
                filter_args = {}
                filter_args["button_filter__contains"] = search_data

                now = datetime.datetime.now()
                nowTime = now.strftime("%M")
                if len(nowTime) == 1:
                    nowTime = "0" + nowTime
                nowTime = nowTime[1:2]
                # print(nowTime)
                target_idx = int(nowTime)
                print(target_idx)
                print(type(target_idx))

                # test_idx??? ???????????? ?????? ??????
                if "test_idx" in self.request.session:
                    if target_idx != self.request.session["test_idx"]:
                        del self.request.session["test_idx"]
                        self.request.session["test_idx"] = target_idx
                else:
                    self.request.session["test_idx"] = target_idx  # 0~6

                sort_idx = self.request.session.get("test_idx")
                if sort_idx == 1:
                    print("sort_idx==1")
                    qs = models.Photo.objects.annotate(random_int_split=Substr("random_int",1)).filter(**filter_args).order_by(
                        "-random_int_split"
                    )
                if sort_idx == 2:
                    print("sort_idx==2")
                    qs = models.Photo.objects.annotate(random_int_split=Substr("random_int",2)).filter(**filter_args).order_by(
                        "-random_int_split"
                    )
                if sort_idx == 3:
                    print("sort_idx==3")
                    qs = models.Photo.objects.annotate(random_int_split=Substr("random_int",3)).filter(**filter_args).order_by(
                        "-random_int_split"
                    )
                if sort_idx == 4:
                    print("sort_idx==4")
                    qs = models.Photo.objects.annotate(random_int_split=Substr("random_int",4)).filter(**filter_args).order_by(
                        "-random_int_split"
                    )
                if sort_idx == 5:
                    print("sort_idx==5")
                    qs = models.Photo.objects.annotate(random_int_split=Substr("random_int",5)).filter(**filter_args).order_by(
                        "-random_int_split"
                    )
                if sort_idx == 6:
                    print("sort_idx==6")
                    qs = models.Photo.objects.annotate(random_int_split=Substr("random_int",5)).filter(**filter_args).order_by(
                        "random_int_split"
                    )
                if sort_idx == 7:
                    print("sort_idx==7")
                    qs = models.Photo.objects.annotate(random_int_split=Substr("random_int",4)).filter(**filter_args).order_by(
                        "random_int_split"
                    )
                if sort_idx == 8:
                    print("sort_idx==8")
                    qs = models.Photo.objects.annotate(random_int_split=Substr("random_int",3)).filter(**filter_args).order_by(
                        "random_int_split"
                    )
                if sort_idx == 9:
                    print("sort_idx==9")
                    qs = models.Photo.objects.annotate(random_int_split=Substr("random_int",2)).filter(**filter_args).order_by(
                        "random_int_split"
                    )
                if sort_idx == 0:
                    print("sort_idx==0")
                    qs = models.Photo.objects.annotate(random_int_split=Substr("random_int",1)).filter(**filter_args).order_by(
                        "random_int_split"
                    )

                paginator = Paginator(qs, 10)
                page = request.GET.get("page", 1)
                photos = paginator.get_page(page)
                if qs.count() > 0:
                    return render(
                        request,
                        "salons/salon_photo_list.html",
                        {"form": form, "photos": photos, "page_obj": photos},
                    )
                elif qs.count() == 0:
                    form = forms.SalonPhotoFilterForm()
                    return render(
                        request,
                        "salons/salon_photo_list.html",
                        {"form": form},
                    )
        form = forms.SalonPhotoFilterForm()
        return render(
            request,
            "salons/salon_photo_list.html",
            {"form": form},
        )