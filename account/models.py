from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        """
        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(
            email=self.normalize_email(email),
            nickname=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, last_name, first_name, password):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여한다.
        """
        user = self.create_user(
            email=email,
            password=password,
            username=username,
        )

        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=_('Email address'),
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        verbose_name=_('Username'),
        max_length=30,
        unique=True
    )
    date_joined = models.DateTimeField(
        verbose_name=_('Date joined'),
        default=timezone.now
    )
    team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True)
    part = models.ForeignKey('Part', on_delete=models.CASCADE, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-date_joined',)

    def __str__(self):
        return self.username


class Team(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Part(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

