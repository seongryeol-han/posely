from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from core import models as core_models

# Create your models here.


class Studio(core_models.TimeStampedModel):
    """Studio Model Definition"""

    name = models.CharField(max_length=50)
    phone_number = PhoneNumberField(default="")
    kakao_chat = models.CharField(max_length=140, blank=True)
    city = models.CharField(max_length=80)
    address = models.CharField(max_length=140)
    open_time = models.TimeField()
    close_time = models.TimeField()
    bio = models.TextField(default="", blank=True)
    file = models.ImageField(upload_to="studio_photos", default="")
    author = models.ForeignKey(
        "users.User",
        related_name="studios",
        limit_choices_to={"studio": True},
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
