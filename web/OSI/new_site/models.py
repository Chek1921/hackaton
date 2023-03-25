from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.base_user import BaseUserManager
from django.urls import reverse_lazy

# Create your models here.

class CustomUserManager(BaseUserManager):
    
    def create_user(self, username, password, **extra_fields):
        
        user = self.model(username = username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password,**extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("allows", '3')

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractUser):
    
    allows = models.CharField("Разрешение", max_length=1, null=False, blank=False, default='1')
    email = models.EmailField("Почта",null=False, blank=False, unique=True)
    want_work = models.BooleanField("Хочет быть админом", default=False)
    work_type = models.ForeignKey("WorkType", on_delete=models.CASCADE, default = 1)

    objects = CustomUserManager()
    REQUIRED_FIELDS = []

class WorkType(models.Model):
    name = models.CharField('Имя', max_length=150, null = False, blank=False)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('work_create')

class TimeFactor(models.Model):
    name = models.CharField('Имя', max_length=150, null = False, blank=False)

    def __str__(self):
        return self.name

class Stage(models.Model):
    name = models.CharField('Имя', max_length=150, null = False, blank=False)

    def __str__(self):
        return self.name


class Report(models.Model):
    userId = models.CharField('Пользователь', max_length=150, null = False, blank=False)
    message = models.TextField('Сообщение', blank=False, null=False)
    work_type = models.ForeignKey('WorkType', on_delete=models.CASCADE, blank = True, null = True)
    time_factor = models.ForeignKey('TimeFactor', on_delete=models.CASCADE, blank = True, null = True)
    stage = models.ForeignKey('Stage', on_delete=models.CASCADE, default= 1)
    address = models.CharField('Адрес', max_length=150, null = False, blank=False)
    whos = models.ForeignKey('CustomUser', on_delete=models.CASCADE, blank=True, null = True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.userId

