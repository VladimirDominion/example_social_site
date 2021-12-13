import uuid

from django.db import models
from django_lifecycle import LifecycleModelMixin, hook, BEFORE_SAVE, AFTER_CREATE
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey

from core.models import path_and_rename, BaseCreatedUpdatedModel


class Tag(LifecycleModelMixin, models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    @hook(BEFORE_SAVE)
    def set_slug(self):
        if not self.slug:
            self.slug = slugify(self.name)


class Post(LifecycleModelMixin, BaseCreatedUpdatedModel):
    # folder name for upload post images for example: /media/posts/<file_name>.jpg
    file_folder = 'posts'
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='posts', blank=True, null=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=250, blank=True, default='')
    text = models.TextField()
    image = models.ImageField(upload_to=path_and_rename, blank=True, default='')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    published = models.BooleanField(default=False, null=True)
    count_likes = models.BigIntegerField(default=0, blank=True, null=True)

    @hook(BEFORE_SAVE)
    def set_slug(self):
        if not self.slug:
            self.slug = f'{slugify(self.title)}_{uuid.uuid4().hex}'


class PostLike(LifecycleModelMixin, BaseCreatedUpdatedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='user_likes')

    @hook(AFTER_CREATE)
    def count_likes(self):
        self.post.count_likes = PostLike.objects.filter(post=self.post).count()
        self.post.save()


class PostComment(MPTTModel, BaseCreatedUpdatedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    published = models.BooleanField(default=False, null=True)

    class MPTTMeta:
        order_insertion_by = ['id']


