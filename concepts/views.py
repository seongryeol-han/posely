from django.views.generic import DetailView, ListView, FormView, UpdateView, View
from django.shortcuts import render, redirect, reverse
from . import models, forms
from django.contrib.auth.decorators import (
    login_required,
)
from users import mixins as user_mixins

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
        return redirect(reverse("core:home"))


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
        return redirect(reverse("core:home"))
