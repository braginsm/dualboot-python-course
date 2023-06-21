from http import HTTPStatus
from typing import Optional
from rest_framework.test import APIClient

from task_manager.main.models.user import User


class ActionClient:
    def __init__(self, api_client: APIClient) -> None:
        self.api_client = api_client
        self.user: Optional[User] = None

    def init_user(self) -> None:
        self.user = User.objects.create()
        self.api_client.force_authenticate(user=self.user)

    def create_task(self, **attributes) -> dict:
        response = self.request_create_task(**attributes)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data
