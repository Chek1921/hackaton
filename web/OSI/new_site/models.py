from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.base_user import BaseUserManager
from django.urls import reverse_lazy
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import datetime



# Create your models her
class UserRating(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    all_rating = models.PositiveSmallIntegerField('Общая оценка')   
    count_raiting = models.PositiveSmallIntegerField('Количество голосов')
    rating = models.FloatField('Оценка', blank = True, null = True)

    def save(self, *args, **kwargs):
        if self.count_raiting != 0:
            self.rating = self.all_rating/self.count_raiting
        super(UserRating, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username
    
class Address(models.Model):
    name = models.CharField('Название', max_length=150, null = False, blank=False)
    residents_count = models.PositiveIntegerField('Количество жильцов')
    payrate = models.PositiveIntegerField('Тариф адреса')
    money = models.PositiveIntegerField('Деньги с адреса', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.money = self.residents_count * self.payrate
        super(Address, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    
    def create_user(self, username, password, **extra_fields):
        
        user = self.model(username = username, **extra_fields)
        user.set_password(password)
        user.save()
        print(user)

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
    work_type = models.ForeignKey("WorkType", on_delete=models.CASCADE, default = 1)

    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)
        if UserRating.objects.filter(user = self):
            pass
        else:
            user_rating = UserRating(
                user = self,
                all_rating = 0,
                count_raiting = 0,
            )
            user_rating.save()

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
    date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null = True)
    cost = models.PositiveIntegerField('Стоимость услуги', blank=True, null = True)

    def __str__(self):
        return self.userId
    
    def notify_ws_clients(self, id):
        """
        Inform client there is a new message.
        """

        using_description = ''
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # desription = {
        #     1: f'Ваша жалоба: \n{self.message}\n\n Находится в состоянии: {self.stage}',
        #     2: f'Ваша жалоба: \n{self.message}\n\n Была взята: {self.whos.username}',
        #     3: f'Ваша жалоба: \n{self.message}\n\n Была выполнена: {self.whos.username}, {now}',
        # }

        # for i in range(3):
        #     if self.stage_id == i+1:
        #         using_description = desription[i]
        #         print(using_description)

        if self.stage_id == 2:
            using_description = f'Ваша жалоба: \n{self.message}\n\n Находится в состоянии: {self.stage} \n Стоимость услуги: {self.cost} тг.'
            rate = False
        elif self.stage_id == 3:
            using_description = f'Ваша жалоба: \n{self.message}\n\n Была взята: {self.whos.first_name}'
            rate = False
        elif self.stage_id == 4:
            using_description = f'Ваша жалоба: \n{self.message}\n\n Была выполнена: {self.whos.first_name}, \n Дата выполнения: {now}'
            rate = True

        notification = {
            'type': 'receive',
            'id': self.id,
            'message': using_description,
            'chat_id': self.userId,
            'rate': rate,
        }

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("chat", notification)

    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        new = self.id
        if new:
            self.notify_ws_clients(new)
        super(Report, self).save(*args, **kwargs)

