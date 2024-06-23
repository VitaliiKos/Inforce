from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.employee.managers import UserManager
from utils.time_stamp import TimeStampedModel


class Employee(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    class Meta:
        db_table = 'employee'

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()
