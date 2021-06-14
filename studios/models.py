from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from core import models as core_models

# Create your models here.


class Studio(core_models.TimeStampedModel):
    """Studio Model Definition"""

    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=11)
    kakao_chat = models.CharField(max_length=140, blank=True)
    address = models.CharField(max_length=140)
    open_time = models.TimeField()
    close_time = models.TimeField()
    introduction = models.TextField(default="", blank=True)
    using_info = models.TextField(default="", blank=True)
    file = models.ImageField(upload_to="studio_photos", default="", blank=True)
    author = models.ForeignKey(
        "users.User",
        related_name="studios",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
