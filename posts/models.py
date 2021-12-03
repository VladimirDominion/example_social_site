from django.db import models
from django_lifecycle import LifecycleModelMixin, hook, BEFORE_SAVE
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey

from core.models import path_and_rename, BaseCreatedUpdatedModel


class Tag(LifecycleModelMixin, models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    @hook(BEFORE_SAVE)
    def set_slug(self):
        self.slug = slugify(self.name)


class Post(LifecycleModelMixin, BaseCreatedUpdatedModel):
    # folder name for upload post images for example: /media/posts/<file_name>.jpg
    file_folder = 'posts'
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    text = models.TextField()
    image = models.ImageField(upload_to=path_and_rename, blank=True, default='')
    tags = models.ManyToManyField(Tag, related_name='posts')
    published = models.BooleanField(default=False, null=True)

    @hook(BEFORE_SAVE)
    def set_slug(self):
        self.slug = slugify(self.name)


class PostComment(MPTTModel, BaseCreatedUpdatedModel):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='posts')
    text = models.TextField()
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    published = models.BooleanField(default=False, null=True)

    class MPTTMeta:
        order_insertion_by = ['id']


