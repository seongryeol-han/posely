from django import forms
from . import models
from PIL import Image


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ("file",)

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        print(photo.file.width)
        image = Image.open(photo.file)
        image_width, image_height = image.size
        print(image_width)
        image = image.resize((400, 404), Image.ANTIALIAS)
        image.save()

        print(photo.file.width)

        concept = models.Concept.objects.get(pk=pk)
        photo.concept = concept
        photo.studio = concept.studio
        photo.save()
