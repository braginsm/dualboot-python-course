from factory import Faker, PostGenerationMethodCall
from factory.django import DjangoModelFactory

from task_manager.main.models.user import User
from test.factories.base import ImageFileProvider

Faker.add_provider(ImageFileProvider)


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    password = PostGenerationMethodCall("set_password", "password")
    role = Faker("random_element", elements=User.Roles.values)
    email = Faker("email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    avatar_picture = Faker("image_file", fmt="jpeg")

    class Meta:
        model = User
