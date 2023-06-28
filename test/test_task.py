from http import HTTPStatus
from test.factories.base import TestViewSetBase
from test.factories.tag_factory import TagFactory
from test.factories.task_factory import TaskFactory

from task_manager.main.models.task import Task
from task_manager.main.serializers import TaskSerializer


class TestTaskViewSet(TestViewSetBase):
    basename = "tasks"
    edit_fields = {"title": "New test task", "description": "new description"}
    except_keys = ["date_update", "date_create"]

    @staticmethod
    def expected_details(entity: dict, attributes: dict) -> dict:
        result = {"id": entity["id"], **attributes}
        return result

    def details_without_keys(self, entity: dict):
        result = entity
        for key in self.except_keys:
            if key in result.keys():
                del result[key]
        return result

    def task_to_dict(self, task: Task) -> dict:
        return self.details_without_keys(TaskSerializer(task).data)

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
        retrieved_task = self.retrieve([created_task["id"]])
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
        new_task = self.update(expected, args=[created_task["id"]])

        assert self.details_without_keys(new_task) == expected

    def test_patch(self):
        task_attributes = TaskFactory.create(tags=(TagFactory.create(),))
        dict_task = self.task_to_dict(task_attributes)
        created_task = self.create(dict_task)
        new_attributes = {**dict_task, **self.edit_fields}
        expected = self.expected_details(created_task, new_attributes)
        new_task = self.update(expected, args=[created_task["id"]])

        assert self.details_without_keys(new_task) == expected

    def test_delete(self):
        task_attributes = TaskFactory.create(tags=(TagFactory.create(),))
        dict_task = self.task_to_dict(task_attributes)
        created_task = self.create(dict_task)
        task_id = created_task["id"]
        self.user.is_staff = True

        assert self.delete(args=[task_id])
        assert self.request_delete(args=[task_id]).status_code == HTTPStatus.NOT_FOUND

    def test_delete_without_permission(self):
        task_attributes = TaskFactory.create(tags=(TagFactory.create(),))
        dict_task = self.task_to_dict(task_attributes)
        created_task = self.create(dict_task)

        assert self.request_delete(args=[created_task["id"]]).status_code == HTTPStatus.FORBIDDEN
