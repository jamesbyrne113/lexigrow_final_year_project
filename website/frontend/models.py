from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class WordInfo(models.Model):
    word = models.CharField(max_length=30)
    pos = models.CharField("part of speech tag", max_length=30, null=True)
    level = models.CharField(max_length=2, null=True)

    class Meta:
        unique_together = ('word', 'pos')


class Details(models.Model):
    word_info = models.ForeignKey(
        WordInfo,
        on_delete=models.CASCADE,
    )
    definition = models.CharField(max_length=300)


class Example(models.Model):
    details = models.ForeignKey(
        Details,
        on_delete=models.CASCADE,
    )
    example = models.CharField(max_length=300)


class LexiGrowUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, email, first_name, last_name, level, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, first_name, last_name, level, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have boolean is_staff set to True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have boolean is_superuser set to True.')

        return self._create_user(email, password, **extra_fields)


class LexiGrowUser(AbstractUser):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    email = models.EmailField('Email Address', unique=True)

    username = models.CharField(max_length=40, unique=False, default='')

    levels = [
        ("A1", "A1"),
        ("A2", "A2"),
        ("B1", "B1"),
        ("B2", "B2"),
        ("C", "C"),
    ]

    objects = LexiGrowUserManager()

    level = models.CharField(max_length=2, choices=levels, default="A1")
    show_harder_words = models.BooleanField('Show Words of All Levels', default=True)

    def __str__(self):
        return self.get_full_name()


class SeenWordInfo(models.Model):
    word_info = models.ForeignKey(
        WordInfo,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        LexiGrowUser,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('word_info', 'user',)
