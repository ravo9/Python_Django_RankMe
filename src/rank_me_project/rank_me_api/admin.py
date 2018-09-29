from __future__ import unicode_literals
from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.UserProfile)
admin.site.register(models.GradeItem)
admin.site.register(models.PictureItem)
