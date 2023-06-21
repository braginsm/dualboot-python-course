from factory import Faker
from factory.django import DjangoModelFactory
from task_manager.main.models.tag import Tag


class TagFactory(DjangoModelFactory):
    title = Faker("user_name")

    class Meta:
        model = Tag
