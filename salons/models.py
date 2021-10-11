from django.db import models
from core import models as core_models
from django.shortcuts import reverse
from django_resized import ResizedImageField
import random

# Create your models here.
class AbstractItem(core_models.TimeStampedModel):
    """Abstract Item"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class SalonBadge(AbstractItem):

    """SalonBadge Model Definition"""

    class Meta:
        verbose_name = "Salon Badge"


class Salon(core_models.TimeStampedModel):
    """Salon Model Definition"""

    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=13, blank=True)
    kakao_chat = models.CharField(max_length=140, blank=True)
    address = models.CharField(max_length=140)
    addr_detail = models.CharField(max_length=140, blank=True)
    addr_short = models.CharField(max_length=140, blank=True)
    location = models.CharField(max_length=140, blank=True)
    location_dong = models.CharField(max_length=140, blank=True)
    open_time = models.TimeField()
    close_time = models.TimeField()
    introduction = models.TextField(default="", blank=True)
    using_info = models.TextField(default="", blank=True)

    salon_avatar = ResizedImageField(
        size=[1024, 1024],
        upload_to="salon_photos",
        quality=95,
        default="",
        blank=True,
        null=True,
    )
    stylist = models.ForeignKey(
        "users.User",
        related_name="salons",
        on_delete=models.CASCADE,
    )

    # 미용실 좋아요 요소
    likes_user = models.ManyToManyField(
        "users.User", blank=True, related_name="salon_likes_user"
    )
    # map
    salon_lat = models.FloatField(blank=True)
    salon_lng = models.FloatField(blank=True)
    salon_badge = models.ManyToManyField(
        "SalonBadge", related_name="salons", blank=True
    )

    def count_likes_user(self):  # 좋아요 수 카운트
        return self.likes_user.count()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("salons:profile", kwargs={"pk": self.pk})

    def all_photo(self):
        photo = self.photos.all()  # ,를 찍으면 파이썬이 첫번째 array 요소를 원하는구나라는것을 알게됨
        return photo

    def first_concept(self):
        try:
            (concept,) = self.concepts.all()[:1]
            return concept
        except ValueError:
            return None


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
    salon = models.ForeignKey(
        "salons.Salon",
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
    salon = models.ForeignKey(
        "salons.Salon",
        related_name="concepts",  # salon에서 concept을 "concepts"으로 사용하면 된다.
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
