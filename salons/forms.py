from django import forms
from . import models

class SalonSearchForm(forms.Form):
    salon_search = forms.CharField(required=False, label="search!")

class CreateConceptForm(forms.ModelForm):
    class Meta:
        model = models.Concept
        fields = (
            "name",
            "service_config",
            "price",
        )

    def save(self, pk, *args, **kwargs):
        concept = super().save(commit=False)
        salon = models.Salon.objects.get(pk=pk)
        concept.salon = salon
        concept.save()
        return concept

class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ("file",)

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        concept = models.Concept.objects.get(pk=pk)
        photo.concept = concept
        photo.salon = concept.salon
        photo.save()
