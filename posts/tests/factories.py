import factory

from posts.models import Tag, Post, PostComment
from users.tests.factories import UserFactory


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.faker.Faker('name')


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.faker.Faker('name')
    text = factory.faker.Faker('text')
    author = factory.SubFactory(UserFactory)


class PostCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PostComment

    text = factory.faker.Faker('text')
    author = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)