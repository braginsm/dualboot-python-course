from task_manager.main.models.tag import Tag
from task_manager.main.models.task import Task
from task_manager.main.models.user import User
from test.base import TestViewSetBase


class TestTaskViewSet(TestViewSetBase):
    basename = "tasks"
    task_attributes = {
        "title": "Test task",
        "description": "Test description",
        "date_deadline": "2023-06-08T06:57:25Z",
        "state": Task.State.IN_DEVELOPMENT,
        "priority": 10,
    }
    edit_fields = {"title": "New test task", "description": "new description"}
    except_keys = ["date_update", "date_create"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.task_attributes["author"] = cls.user.id
        cls.task_attributes["assigned"] = cls.user.id
        cls.task_attributes["tags"] = [Tag.objects.create(title="Test tag").id]

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {"id": entity["id"], **attributes}

    def details_without_keys(self, entity: dict):
        result = entity
        for key in self.except_keys:
            if key in result.keys():
                del result[key]
        return result

    def test_create(self):
        task = self.create(self.task_attributes)
        expected_response = self.expected_details(task, self.task_attributes)
        assert self.details_without_keys(task) == expected_response

    def test_get_by_id(self):
        task = self.create(self.task_attributes)
        task_id = task["id"]
        compare_task = self.get_by_id(task_id)
        assert self.details_without_keys(compare_task) == self.expected_details(
            task, self.task_attributes
        )

    def test_get_tasks(self):
        task = self.create(self.task_attributes)
        response = self.get_list()
        tasks = self.response_to_list_dict(response, self.details_without_keys)
        assert self.expected_details(task, self.task_attributes) in tasks

    def test_put_task(self):
        task = self.create(self.task_attributes)
        expected = self.details_without_keys({**task, **self.edit_fields})
        new_task = self.put_by_id(expected, task["id"])
        assert self.details_without_keys(new_task) == expected

    def test_patch_task(self):
        task = self.create(self.task_attributes)
        expected = self.details_without_keys({**task, **self.edit_fields})
        new_task = self.patch_by_id(self.edit_fields, task["id"])
        assert self.details_without_keys(new_task) == expected

    def test_delete_task(self):
        task = self.create(self.task_attributes)
        task_id = task["id"]
        assert self.delete_by_id(task_id)
        assert not self.delete_by_id(task_id)

    def test_delete_task_without_permission(self):
        task = self.create(self.task_attributes)
        user = User.objects.create_user("test2@test.ru", email=None, password=None)
        assert not self.delete_by_id(task["id"], user)
