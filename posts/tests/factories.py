import factory

from posts.models import Tag, Post, PostComment



class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.faker.Faker('name')


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.faker.Faker('title')
    text = factory.faker.Faker('text')


class PostCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PostComment

    text = factory.faker.Faker('text')