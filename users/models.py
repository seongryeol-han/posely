from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import SET_NULL
from phonenumber_field.modelfields import PhoneNumberField
from django.shortcuts import reverse
from core import managers as core_managers
from imagekit.models import ProcessedImageField

# Create your models here.


class User(AbstractUser):

    """Custom User Model"""

    LOGIN_EMAIL = "email"
    LOGIN_NAVER = "naver"
    LOGING_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_NAVER, "naver"),
        (LOGING_KAKAO, "Kakao"),
    )

    avatar = ProcessedImageField(
        upload_to="avatars",
        blank=True,
        default="",
        format="JPEG",
        options={"quality": 60},
    )
    phone_number = models.CharField(max_length=11)
    nickname = models.CharField(
        max_length=30,
        null=False,
        unique=True,
        error_messages={
            "unique": "이미 존재하는 닉네임입니다.",
        },
    )
    petname = models.CharField(max_length=30, blank=True)
    studio = models.BooleanField(default=False)
    bio = models.TextField(default="", blank=True)

    # 05.09 social login check
    email_verified = models.BooleanField(default=False)

    has_studio = models.ForeignKey(
        "studios.Studio",
        related_name="has_studio",
        on_delete=SET_NULL,
        blank=True,
        null=True,
    )

    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    objects = core_managers.CustomUserManager()

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

    # def count_has_studio(self):  # 좋아요 수 카운트
    #     if self.has_studio is None:
    #         return True
    #     else:
    #         return False
