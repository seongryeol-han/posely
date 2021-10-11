from django import forms
from . import models
from concepts import models as concept_model

class StudioSearchForm(forms.Form):
    studio_search = forms.CharField(required=False, label="search!")


class CreateStudioForm(forms.ModelForm):
    class Meta:
        model = models.Studio
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

    def save(self, *args, **kwargs):
        studio = super().save(commit=False)  # commit=False의 의미는 지금 당장 DB에 저장하지 않는다.
        return studio


class CreateConceptForm(forms.ModelForm):
    class Meta:
        model = concept_model.Concept
        fields = (
            "name",
            "service_config",
            "price",
        )

    def save(self, pk, *args, **kwargs):
        concept = super().save(commit=False)
        studio = models.Studio.objects.get(pk=pk)
        concept.studio = studio
        concept.save()
        return concept
