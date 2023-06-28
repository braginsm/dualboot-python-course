from task_manager.main.models.task import Task
from test.base import TestViewSetBase


class TestUserTasksViewSet(TestViewSetBase):
    basename = "task_tags"

    def test_list(self) -> None:
        task = self.action_client.create_task(assigned_id=self.user.id)
        tag1 = self.action_client.create_tag()
        tag2 = self.action_client.create_tag()
        self.add_tags(task, [tag1, tag2])

        tags = self.response_to_list_dict(self.list(args=[task["id"]]))
        assert tag1 in tags and tag2 in tags

    def add_tags(self, task: dict, tags: list[dict]) -> None:
        task_instance = Task.objects.get(pk=task["id"])
        for tag in tags:
            task_instance.tags.add(tag["id"])
        task_instance.save()
