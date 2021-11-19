from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractUser
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.db import models
from django_lifecycle import BEFORE_SAVE, LifecycleModelMixin, hook, AFTER_CREATE

from core.models import path_and_rename


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        validate_email(email)
        validate_password(password)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(LifecycleModelMixin, AbstractBaseUser, PermissionsMixin):
    class SEX(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'Female'
        ANOTHER = 'ANOTHER', 'Another'

    file_folder = 'images'
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    avatar = models.ImageField(upload_to=path_and_rename, blank=True, null=True)

    date_of_birth = models.DateField(null=True, blank=True)
    about_me = models.CharField(max_length=1024, blank=True)
    sex = models.CharField(max_length=10, blank=True, default="", choices=SEX.choices)

    date_joined = models.DateField(auto_now_add=True)

    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user '
                  'can log into this admin site.'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Designates whether this user should be treated as active. '
                  'Unselect this instead of deleting accounts.'
    )
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{str(self.full_name)}'

    class Meta:
        ordering = ['-date_joined']

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip() \
            if self.first_name or self.last_name else self.email

    # lifecycle hooks

    @hook(AFTER_CREATE)
    def user_created(self):
        """ Do some staff after create """

