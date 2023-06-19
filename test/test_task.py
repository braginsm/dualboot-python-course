import datetime
from http import HTTPStatus
from task_manager.main.models.task import Task
from task_manager.main.serializers import TaskSerializer
from test.factories.base import TestViewSetBase
from test.factories.tag_factory import TagFactory
from test.factories.task_factory import TaskFactory


class TestTaskViewSet(TestViewSetBase):
    basename = "tasks"
    fields = TaskSerializer.Meta.fields
    edit_fields = {"title": "New test task", "description": "new description"}
    except_keys = ["date_update", "date_create"]

    # @classmethod
    # def setUpTestData(cls) -> None:
    #     super().setUpTestData()
    #     cls.task_attributes["author"] = cls.user.id
    #     cls.task_attributes["assigned"] = cls.user.id
    #     cls.task_attributes["tags"] = [Tag.objects.create(title="Test tag").id]

    @staticmethod
    def expected_details(entity: dict, attributes: dict) -> dict:
        result = {
            "id": entity["id"],
            **attributes,
            "assigned": attributes["assigned_id"],
            "author": attributes["author_id"],
        }
        del result["assigned_id"]
        del result["author_id"]
        return result

    def details_without_keys(self, entity: dict):
        result = entity
        for key in self.except_keys:
            if key in result.keys():
                del result[key]
        return result

    def task_to_dict(self, task: Task) -> dict:
        result = task.__dict__
        result["author"] = task.author.id
        result["assigned"] = task.assigned.id
        result["tags"] = list(map(lambda tag: tag.id, task.tags.all()))
        result["date_deadline"] = task.date_deadline.strftime("%Y-%m-%dT%H:%M:%SZ")
        result["state"] = str(task.state)
        del result["_state"]
        return self.details_without_keys(result)

    def test_create(self) -> None:
        task_attributes = TaskFactory.create(tags=(TagFactory.create(),))
        dict_task = self.task_to_dict(task_attributes)
        created_task = self.create(dict_task)
        expected_response = self.expected_details(created_task, dict_task)

        assert self.details_without_keys(created_task) == expected_response

    def test_retrieve(self) -> None:
        task_attributes = TaskFactory.create(tags=(TagFactory.create(),))
        dict_task = self.task_to_dict(task_attributes)
        created_task = self.create(dict_task)
        retrieved_task = self.retrieve(created_task["id"])
        expected_response = self.expected_details(created_task, dict_task)

        assert self.details_without_keys(retrieved_task) == expected_response

    def test_list(self):
        task_attributes = TaskFactory.create(tags=(TagFactory.create(),))
        dict_task = self.task_to_dict(task_attributes)
        created_task = self.create(dict_task)
        response = self.list()
        tags = self.response_to_list_dict(response, self.details_without_keys)

        assert self.expected_details(created_task, dict_task) in tags

    def test_update(self):
        task_attributes = TaskFactory.create(tags=(TagFactory.create(),))
        dict_task = self.task_to_dict(task_attributes)
        created_task = self.create(dict_task)
        new_attributes = {**dict_task, **self.edit_fields}
        expected = self.expected_details(created_task, new_attributes)
        new_task = self.update(expected, created_task["id"])

        assert self.details_without_keys(new_task) == expected

    def test_patch(self):
        task_attributes = TaskFactory.create(tags=(TagFactory.create(),))
        dict_task = self.task_to_dict(task_attributes)
        created_task = self.create(dict_task)
        new_attributes = {**dict_task, **self.edit_fields}
        expected = self.expected_details(created_task, new_attributes)
        new_task = self.update(expected, created_task["id"])

        assert self.details_without_keys(new_task) == expected

    def test_delete(self):
        task_attributes = TaskFactory.create(tags=(TagFactory.create(),))
        dict_task = self.task_to_dict(task_attributes)
        created_task = self.create(dict_task)
        task_id = created_task["id"]
        self.user.is_staff = True

        assert self.delete(task_id)
        assert self.request_delete(task_id).status_code == HTTPStatus.NOT_FOUND

    def test_delete_without_permission(self):
        task_attributes = TaskFactory.create(tags=(TagFactory.create(),))
        dict_task = self.task_to_dict(task_attributes)
        created_task = self.create(dict_task)

        assert (
            self.request_delete(created_task["id"]).status_code == HTTPStatus.FORBIDDEN
        )
