from django.views.generic import DetailView, ListView, FormView, UpdateView, View
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from . import models, forms
from django.contrib.auth.decorators import (
    login_required,
)
from users import mixins as user_mixins
import datetime, random

# Create your views here.


class ConceptDetail(DetailView):
    """ConceptDetail Definition"""

    model = models.Concept


class ConceptEditListView(ListView):

    """HomeView Definition"""

    template_name = "concepts/concept_edit-list.html"
    model = models.Concept
    ordering = "created"
    context_object_name = "concepts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EditConceptView(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.Concept
    template_name = "concepts/concept_edit.html"
    fields = (
        "name",
        "concept_description",
        "service_config",
        "price",
    )

    def form_valid(self, form):
        pk = self.kwargs.get("pk")  # form으로 pk를 갖다줘야해서 pk를 설정 (concept의 pk).
        form.save(pk)  # pk를 줌 form에다가
        return redirect(reverse("concepts:edit-list"))

    def get_object(self, queryset=None):
        concept = super().get_object(queryset=queryset)
        if concept.studio.author.pk != self.request.user.pk:
            raise Http404()
        return concept

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        form.fields["name"].label = "컨셉 이름"
        form.fields["concept_description"].label = "컨셉 설명"
        form.fields["service_config"].label = "컨셉 이용안내"
        form.fields["price"].label = "가격"
        return form


class ConceptPhotosView(user_mixins.LoggedInOnlyView, DetailView):
    model = models.Concept
    template_name = "concepts/concept_photos.html"

    def get_object(self, queryset=None):  # 룸 호스트랑 요청하는 사람이랑 같은지
        concept = super().get_object(queryset=queryset)
        if concept.studio.author.pk != self.request.user.pk:
            raise Http404()
        return concept


@login_required  # 만약 로그인이 안되어 있으면, setting에서 LOGIN_URL 로 이동한다 (이거 설정해둬야함.)
def delete_photo(request, concept_pk, photo_pk):  # url.py에 등록되어있는거.
    user = request.user
    try:
        concept = models.Concept.objects.get(pk=concept_pk)
        if concept.studio.author.pk != user.pk:
            Http404()
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
        return redirect(reverse("concepts:photos", kwargs={"pk": concept_pk}))
    except models.Concept.DoesNotExist:  # concept이 없음
        return redirect(reverse("core:photo_home"))


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):

    model = models.Photo
    template_name = "concepts/photo_create.html"
    fields = "file"
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")  # form으로 pk를 갖다줘야해서 pk를 설정 (concept의 pk).
        form.save(pk)  # pk를 줌 form에다가
        return redirect(reverse("concepts:photos", kwargs={"pk": pk}))


@login_required  # 만약 로그인이 안되어 있으면, setting에서 LOGIN_URL 로 이동한다 (이거 설정해둬야함.)
def delete_concept(request, concept_pk):  # url.py에 등록되어있는거.
    user = request.user
    try:
        concept = models.Concept.objects.get(pk=concept_pk)
        if concept.studio.author.pk != user.pk:
            Http404()
        else:
            models.Concept.objects.filter(pk=concept_pk).delete()
        return redirect(reverse("concepts:edit-list"))
    except models.Concept.studio.DoesNotExist:  # concept이 없음
        return redirect(reverse("core:photo_home"))


class PhotoHomeView(ListView):
    """photoHomeView Definition"""

    model = models.Photo
    paginate_by = 10
    context_object_name = "photos"
    template_name = "photos/photo_list.html"

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

        # test_idx가 세션있나 없나 체크
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
            ps_with_avg = models.Photo.objects.all().order_by("random_int")
        if sort_idx == 2:
            print("sort_idx==2")
            ps_with_avg = models.Photo.objects.all().order_by("-random_int")
        if sort_idx == 3:
            print("sort_idx==3")
            ps_with_avg = models.Photo.objects.all().order_by("random_int")
        if sort_idx == 4:
            print("sort_idx==4")
            ps_with_avg = models.Photo.objects.all().order_by("random_int")
        if sort_idx == 5:
            print("sort_idx==5")
            ps_with_avg = models.Photo.objects.all().order_by("random_int")
        if sort_idx == 6:
            print("sort_idx==6")
            ps_with_avg = models.Photo.objects.all().order_by("random_int")
        if sort_idx == 7:
            print("sort_idx==7")
            ps_with_avg = models.Photo.objects.all().order_by("random_int")
        if sort_idx == 8:
            print("sort_idx==8")
            ps_with_avg = models.Photo.objects.all().order_by("random_int")
        if sort_idx == 9:
            print("sort_idx==9")
            ps_with_avg = models.Photo.objects.all().order_by("random_int")
        if sort_idx == 0:
            print("sort_idx==0")
            ps_with_avg = models.Photo.objects.all().order_by("random_int")
        return ps_with_avg


class ButtonFilterView(View):
    """SearchView Definition"""

    def get(self, request):
        form = forms.PhotoFilterForm(request.GET)
        if form.is_valid():
            search_data = form.cleaned_data.get("photo_filter")
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

                # test_idx가 세션있나 없나 체크
                if "test_idx" in self.request.session:
                    if target_idx != self.request.session["test_idx"]:
                        del self.request.session["test_idx"]
                        self.request.session["test_idx"] = target_idx
                else:
                    self.request.session["test_idx"] = target_idx  # 0~6

                sort_idx = self.request.session.get("test_idx")
                if sort_idx == 1:
                    print("sort_idx==1")
                    qs = models.Photo.objects.filter(**filter_args).order_by(
                        "random_int"
                    )
                if sort_idx == 2:
                    print("sort_idx==2")
                    qs = models.Photo.objects.filter(**filter_args).order_by("random_int")
                if sort_idx == 3:
                    print("sort_idx==3")
                    qs = models.Photo.objects.filter(**filter_args).order_by("random_int")
                if sort_idx == 4:
                    print("sort_idx==4")
                    qs = models.Photo.objects.filter(**filter_args).order_by("random_int")
                if sort_idx == 5:
                    print("sort_idx==5")
                    qs = models.Photo.objects.filter(**filter_args).order_by("random_int")
                if sort_idx == 6:
                    print("sort_idx==6")
                    qs = models.Photo.objects.filter(**filter_args).order_by("random_int")
                if sort_idx == 7:
                    print("sort_idx==7")
                    qs = models.Photo.objects.filter(**filter_args).order_by(
                        "random_int"
                    )
                if sort_idx == 8:
                    print("sort_idx==8")
                    qs = models.Photo.objects.filter(**filter_args).order_by("random_int")
                if sort_idx == 9:
                    print("sort_idx==9")
                    qs = models.Photo.objects.filter(**filter_args).order_by("random_int")
                if sort_idx == 0:
                    print("sort_idx==0")
                    qs = models.Photo.objects.filter(**filter_args).order_by("random_int")

                paginator = Paginator(qs, 10, orphans=3)
                page = request.GET.get("page", 1)
                photos = paginator.get_page(page)
                if qs.count() > 0:
                    return render(
                        request,
                        "photos/photo_list.html",
                        {"form": form, "photos": photos},
                    )
                elif qs.count() == 0:
                    form = forms.PhotoFilterForm()
                    return render(
                        request,
                        "photos/photo_list.html",
                        {"form": form},
                    )
        form = forms.PhotoFilterForm()
        return render(
            request,
            "photos/photo_list.html",
            {"form": form},
        )
