from django.db import models
from core import models as core_models
from django_resized import ResizedImageField
import random

# Create your models here.


class Photo(core_models.TimeStampedModel):
    """Photo Model Definition"""

    caption = models.CharField(max_length=80, default="", blank=True)
    # file = models.ImageField(
    #     upload_to="concept_photos",
    # )

    button_filter = models.CharField(max_length=80, default="", blank=True)

    file = ResizedImageField(
        size=[1024, 1024],
        upload_to="concept_photos",
        quality=95,
    )
    concept = models.ForeignKey(
        "Concept", related_name="photos", on_delete=models.CASCADE
    )
    studio = models.ForeignKey(
        "studios.Studio",
        related_name="photos",
        on_delete=models.CASCADE,
        default="",
        blank=True,
    )

    def random_string():
        return str(random.randint(100000, 999999))

    random_int = models.CharField(max_length=6, default=random_string, blank=True)

    def __str__(self):
        return self.caption


class Concept(core_models.TimeStampedModel, models.Model):
    """Concept Model Definition"""

    name = models.CharField(max_length=15)
    concept_description = models.TextField(max_length=160, default="", blank=True)
    service_config = models.TextField(default="", blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=0)
    studio = models.ForeignKey(
        "studios.Studio",
        related_name="concepts",  # studio에서 concept을 "concepts"으로 사용하면 된다.
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    def all_photo(self):
        photo = self.photos.all()  # ,를 찍으면 파이썬이 첫번째 array 요소를 원하는구나라는것을 알게됨
        return photo

    def first_photo(self):
        try:  # try한 이유는. concept을 만들 때 사진을 안넣어주면 에러가 나서 사진이 없더라도 그냥 return None 내보내게 함.
            (photo,) = self.photos.all()[:1]
            return photo.file
        except ValueError:
            return None
