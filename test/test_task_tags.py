from test.factories.base import TestViewSetBase
from test.factories.tag_factory import TagFactory

from task_manager.main.models.task import Task
from task_manager.main.serializers import TagSerializer


class TestUserTasksViewSet(TestViewSetBase):
    basename = "task_tags"

    def test_list(self) -> None:
        task = self.action_client.create_task(assigned_id=self.user.id)
        tag1 = self.action_client.create_tag()
        tag2 = self.action_client.create_tag()
        self.add_tags(task, [tag1, tag2])

        tags = self.response_to_list_dict(self.list(args=[task["id"]]))
        assert tag1 in tags and tag2 in tags

    @staticmethod
    def add_tags(task: dict, tags: list[dict]) -> None:
        task_instance = Task.objects.get(pk=task["id"])
        for tag in tags:
            task_instance.tags.add(tag["id"])
        task_instance.save()

    def test_delete(self) -> None:
        self.user.is_staff = True
        task = self.action_client.create_task(assigned_id=self.user.id)
        tag = self.action_client.create_tag()
        self.add_tags(task, [tag])

        tags = self.response_to_list_dict(self.list(args=[task["id"]]))
        assert tag in tags
        
        self.delete(args=[task["id"], tag['id']])
        tags = self.response_to_list_dict(self.list(args=[task["id"]]))
        assert tag not in tags
        
    def test_update(self):
        task = self.action_client.create_task(assigned_id=self.user.id)
        tag = self.action_client.create_tag()
        self.add_tags(task, [tag])
        new_attributes = {**tag, **{'title': 'new title'}}
        new_tag = self.update(new_attributes, [task['id'], tag["id"]])

        assert new_tag == new_attributes
        
    def test_create(self) -> None:
        task = self.action_client.create_task(assigned_id=self.user.id)
        tag_attributes = TagSerializer(TagFactory.build()).data
        tag = self.create(tag_attributes, args=[task['id']])
        expected_response = {**tag_attributes, 'id': tag['id']}

        assert tag == expected_response
        tags = self.response_to_list_dict(self.list(args=[task["id"]]))
        assert expected_response in tags
