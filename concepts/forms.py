from django import forms
from . import models


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ("file",)

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        concept = models.Concept.objects.get(pk=pk)
        photo.concept = concept
        photo.studio = concept.studio
        photo.save()


class StudioPhotoFilterForm(forms.Form):
    photo_filter = forms.CharField(required=False)
