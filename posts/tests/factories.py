import factory

from posts.models import Tag


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.faker.Faker('name')