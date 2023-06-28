from http import HTTPStatus
from test.base import TestViewSetBase


class TestUserTasksViewSet(TestViewSetBase):
    basename = "user_tasks"

    def test_list(self) -> None:
        self.action_client.create_task(assigned_id=self.user.id)
        user = self.action_client.create_user()
        task1 = self.action_client.create_task(assigned_id=user["id"])
        tasks = self.list(args=[user["id"]])

        assert tasks == [task1]

    def test_retrieve(self) -> None:
        user = self.action_client.create_user()
        created_task = self.action_client.create_task(assigned_id=user["id"])
        retrieved_task = self.retrieve(args=[user["id"], created_task["id"]])

        assert created_task == retrieved_task

    def test_retrieve_foreign_task(self) -> None:
        user = self.action_client.create_user()
        task = self.action_client.create_task(assigned_id=self.user.id)
        response = self.request_retrieve(args=[user["id"], task["id"]])

        assert response.status_code == HTTPStatus.NOT_FOUND
