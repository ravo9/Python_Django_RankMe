from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserProfileManager(BaseUserManager):
    """Helps Django work with our custom Profile model."""

    def create_user(self, email, name, password=None):
        """Creates a new Profile object."""
        if not email:
            raise ValueError('User profile must have an e-mail address.')
        email   = self.normalize_email(email)
        profile = self.model(email=email, name=name)
        # This function will encrypt a password for us.
        profile.set_password(password)
        profile.save(using=self._db)
        return profile

    def create_superuser(self, email, name, password):
        """Creates a new super user profile with given details."""
        profile = self.create_user(email, name, password)
        profile.is_superuser = True
        profile.is_staff = True
        profile.save(using=self._db)
        return profile


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Represents a user profile inside our system."""

    email                   = models.EmailField(max_length=255, unique=True)
    name                    = models.CharField(max_length=255)
    age                     = models.IntegerField(null=True, blank=True)
    gender                  = models.CharField(max_length=255, blank=True)
    main_profile_picture    = models.ForeignKey('PictureItem', null=True, blank=True, on_delete=models.SET_NULL)
    is_active               = models.BooleanField(default=True)
    is_staff                = models.BooleanField(default=False)
    objects                 = UserProfileManager()
    USERNAME_FIELD          = 'email'
    REQUIRED_FIELDS         = ['name']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email


class PictureItem(models.Model):
    """A picture object."""

    profile         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status_text     = models.CharField(max_length=255, null=True, blank=True)
    picture         = models.ImageField(upload_to='pictures')
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status_text


class GradeItem(models.Model):
    """A picture's grade."""

    picture         = models.ForeignKey('PictureItem', on_delete=models.CASCADE)
    status_text     = models.CharField(max_length=255, null=True, blank=True)
    grading_profile = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    grade           = models.IntegerField()
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status_text
