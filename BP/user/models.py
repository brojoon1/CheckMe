from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password

#유저 매니저 커스텀
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, phone=None, email=None, name=None, img_src=None, nickname=None, pw_date=None, create_date=None, **extra_fields):
        user = self.model(
            username=username,
            phone=phone,
            email=email,
            name=name,
            img_src=img_src,
            nickname=nickname,
            pw_date=pw_date,
            create_date=create_date,
            **extra_fields
        )
        user.save(using=self._db)
        return user

#superuser 생성(세부 필드는 하드코딩)
    def create_superuser(self, username, password=None, phone=None, email=None, name=None, img_src=None, nickname=None, pw_date=None, create_date=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(
            username=username,
            password=password,
            phone='admin',
            email='admin',
            name='admin',
            img_src='https://w7.pngwing.com/pngs/441/722/png-transparent-pikachu-thumbnail.png',
            nickname='admin',
            pw_date='2022-03-15 10:32:47.382549',
            create_date='2022-03-15 10:32:47.382549',
            **extra_fields
        )
class User(AbstractBaseUser):
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
    ]
    
    username = models.CharField(max_length=200, unique=True, default='')
    password = models.CharField(max_length=128, default='')
    phone = models.CharField(max_length=15, blank=False, null=False)
    email = models.CharField(max_length=30, blank=False, null=False)
    name = models.CharField(max_length=10, blank=False, null=False)
    img_src = models.CharField(max_length=100, default='https://w7.pngwing.com/pngs/441/722/png-transparent-pikachu-thumbnail.png')
    nickname = models.CharField(max_length=16, unique=False)
    pw_date = models.DateTimeField(default=timezone.now)
    create_date = models.DateTimeField(default=timezone.now)
    birth = models.DateField(null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return raw_password == self.password

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    

class user_favor(models.Model):
    username = models.CharField(max_length=200, unique=True)
    favor1 = models.CharField(max_length=30)
    favor2 = models.CharField(max_length=30)
    favor3 = models.CharField(max_length=30)
    favor4 = models.CharField(max_length=30)