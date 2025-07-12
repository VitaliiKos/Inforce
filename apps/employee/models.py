import os

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.core import validators as V

from apps.employee.managers import UserManager
from utils.enums.regex_enum import RegEx
from utils.services.upload_avatar_service import upload_to
from utils.time_stamp import TimeStampedModel


class Employee(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    class Meta:
        db_table = 'employee'
        ordering = ('-created_at',)

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128,
                                validators=[V.RegexValidator(RegEx.PASSWORD.pattern, RegEx.PASSWORD.msg)])
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()


class UserProfile(TimeStampedModel):
    class Meta:
        db_table = 'profile'
        ordering = ('-created_at',)

    first_name = models.CharField(max_length=20,
                                  validators=[V.RegexValidator(RegEx.FIRST_NAME.pattern, RegEx.FIRST_NAME.msg)])
    last_name = models.CharField(max_length=20,
                                 validators=[V.RegexValidator(RegEx.LAST_NAME.pattern, RegEx.LAST_NAME.msg)])
    phone = models.CharField(max_length=20, blank=True,
                             validators=[V.RegexValidator(RegEx.PHONE.pattern, RegEx.PHONE.msg)])
    avatar = models.ImageField(upload_to=upload_to, blank=True)
    user = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='profile')

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_instance = UserProfile.objects.get(pk=self.pk)
                if old_instance.avatar and self.avatar != old_instance.avatar:
                    if os.path.isfile(old_instance.avatar.path):
                        os.remove(old_instance.avatar.path)
            except UserProfile.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.avatar:
            if os.path.isfile(self.avatar.path):
                os.remove(self.avatar.path)
        super().delete(*args, **kwargs)