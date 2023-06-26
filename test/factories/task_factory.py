import factory
from factory.django import DjangoModelFactory

from task_manager.main.models.task import Task
from task_manager.main.models.user import User


class TaskFactory(DjangoModelFactory):
    author = factory.Iterator(User.objects.all())
    assigned_id = factory.Iterator(User.objects.all(), getter=lambda user: user.id)
    date_create = factory.Faker("date_time")
    date_update = factory.Faker("date_time")
    date_deadline = factory.Faker("future_datetime")
    description = factory.Faker("text")
    title = factory.Faker("name")

    class Meta:
        model = Task

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.tags.add(group)
