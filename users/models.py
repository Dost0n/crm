from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta, datetime
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from utils.models import BaseModel
from .managers import UserManager
import random


USER, ADMIN, SUPERADMIN = ("user", 'admin', 'superadmin')
ACTIVE, DEACTIVE = ("active", 'deactive')
PHONE_EXPIRE_MINUTE = 2


class User(AbstractUser, BaseModel):
    USER_ROLES = (
        (USER, USER),
        (ADMIN, ADMIN),
        (SUPERADMIN, SUPERADMIN)
    )

    AUTH_STATUS = (
        (ACTIVE, ACTIVE),
        (DEACTIVE, DEACTIVE),
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    username = None
    email = None

    user_role = models.CharField(
        max_length=31, choices=USER_ROLES, default=USER)
    auth_status = models.CharField(
        max_length=31, choices=AUTH_STATUS, default=ACTIVE)
    phone_number = models.CharField(
        max_length=13, null=True, blank=True, unique=True)

    objects = UserManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name
