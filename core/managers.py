from django.db import models
from django.contrib.auth.models import UserManager


class CustomModelManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class CustomUserManager(CustomModelManager, UserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        user = self.model(email=email, username=username, is_staff=True,
                          is_superuser=True, nickname="master-nick0")
        user.set_password(password)
        user.save()
        return user
