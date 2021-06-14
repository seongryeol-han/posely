from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

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

    avatar = models.ImageField(upload_to="avatars", blank=True)
    phone_number = models.CharField(max_length=11)
    nickname = models.CharField(
        max_length=30,
        null=False,
        unique=True,
        error_messages={
            "unique": "A user with that nickname already exists.",
        },
    )
    petname = models.CharField(max_length=30, blank=True)
    studio = models.BooleanField(default=False)
    bio = models.TextField(default="", blank=True)

    # 05.09 social login check
    email_verified = models.BooleanField(default=False)

    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )
