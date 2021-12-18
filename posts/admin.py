from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Post, PostComment


class CommentsInline(admin.StackedInline):
    model = PostComment
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CommentsInline]


# @admin.register(PostComment, MPTTModelAdmin)
# class PostCommentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'post', 'author', 'text')

