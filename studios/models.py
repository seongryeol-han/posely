from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from core import models as core_models
from django.shortcuts import reverse
from django_resized import ResizedImageField

# Create your models here.


class Studio(core_models.TimeStampedModel):
    """Studio Model Definition"""

    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=13)
    kakao_chat = models.CharField(max_length=140, blank=True)
    address = models.CharField(max_length=140)
    addr_detail = models.CharField(max_length=140, blank=True)
    addr_short = models.CharField(max_length=140, blank=True)
    open_time = models.TimeField()
    close_time = models.TimeField()
    introduction = models.TextField(default="", blank=True)
    using_info = models.TextField(default="", blank=True)
    # studio_avatar = models.ImageField(
    #     upload_to="studio_photos", default="", blank=True, null=True
    # )
    studio_avatar = ResizedImageField(
        size=[1024, 1024],
        upload_to="studio_photos",
        quality=95,
        default="",
        blank=True,
        null=True,
    )
    author = models.ForeignKey(
        "users.User",
        related_name="studios",
        on_delete=models.CASCADE,
    )

    # 스듀디오 좋아요 요소
    likes_user = models.ManyToManyField(
        "users.User", blank=True, related_name="likes_user"
    )
    # map
    studio_lat = models.FloatField(blank=True)
    studio_lng = models.FloatField(blank=True)

    def count_likes_user(self):  # 좋아요 수 카운트
        return self.likes_user.count()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("studios:profile", kwargs={"pk": self.pk})

    def all_photo(self):
        photo = self.photos.all()  # ,를 찍으면 파이썬이 첫번째 array 요소를 원하는구나라는것을 알게됨
        return photo

    def first_concept(self):
        try:
            (concept,) = self.concepts.all()[:1]
            return concept
        except ValueError:
            return None
