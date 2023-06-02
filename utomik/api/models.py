import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, birthdate, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("User must have an email address.")
        if not username:
            raise ValueError("User must have a username.")
        if not birthdate:
            raise ValueError("User must have a birthdate.")

        user = self.model(email=self.normalize_email(email),
                          username=username,
                          birthdate=birthdate
                          )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, birthdate, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email=self.normalize_email(email),
                                username=username,
                                birthdate=birthdate,
                                password=password,
                                )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    birthdate = models.DateField()
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username", "birthdate"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True


class Game(models.Model):
    name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)


class PlaySession(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
