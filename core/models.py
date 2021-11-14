from django.db import models
from django.utils import timezone
import os
from uuid import uuid4


def path_and_rename(instance, filename):
    upload_to = 'images' if not instance.file_folder else instance.file_folder
    ext = filename.split('.')[-1]
    # get filename
    filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class BaseCreatedUpdatedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
