from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from apps.common.models import BaseModel, UUIDModel, SoftDeleteModel
from apps.users.manager import UserManager
from apps.users.services.avatar_uploader import user_avatar_path


class User(AbstractBaseUser, PermissionsMixin, BaseModel, UUIDModel, SoftDeleteModel):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True)
    settings = models.JSONField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
