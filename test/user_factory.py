from factory import PostGenerationMethodCall
from factory.django import DjangoModelFactory
from faker import Faker

from task_manager.main.models.user import User


class UserFactory(DjangoModelFactory):
    username = Faker().user_name()
    password = PostGenerationMethodCall("set_password", "password")

    class Meta:
        model = User
