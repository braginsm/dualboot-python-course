from http import HTTPStatus
from typing import Optional
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.response import Response

from task_manager.main.models.user import User
from task_manager.main.serializers import TagSerializer, TaskSerializer, UserSerializer
from test.factories.tag_factory import TagFactory
from test.factories.task_factory import TaskFactory
from test.factories.user_factory import UserFactory


class ActionClient:
    def __init__(self, api_client: APIClient) -> None:
        self.api_client = api_client
        self.user: Optional[User] = None

    def init_user(self) -> None:
        self.user = User.objects.create()
        self.api_client.force_authenticate(user=self.user)

    def create_task(self, **attributes) -> dict:
        if "author" not in attributes and "author_id" not in attributes:
            attributes["author"] = self.user
        response = self.request_create_task(**attributes)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def request_create_task(self, **attributes) -> Response:
        if "tags" not in attributes or not attributes["tags"]:
            fake_tag = TagFactory.build()
            fake_tag.id = self.create_tag(**TagSerializer(fake_tag).data)["id"]
            attributes["tags"] = [fake_tag.id]
        fake_task = TaskSerializer(TaskFactory.build(**attributes)).data
        del fake_task["id"]
        fake_task["tags"] = attributes["tags"]
        return self.api_client.post(reverse(f"tasks-list"), data=fake_task)

    def create_tag(self, **attributes) -> dict:
        response = self.request_create_tag(**attributes)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def request_create_tag(self, **attributes) -> Response:
        fake_user = TagSerializer(TagFactory.build(**attributes)).data
        del fake_user["id"]
        return self.api_client.post(reverse(f"tags-list"), data=fake_user)

    def create_user(self, **attributes) -> dict:
        response = self.request_create_user(**attributes)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def request_create_user(self, **attributes) -> Response:
        fake_user = UserSerializer(UserFactory.build(**attributes)).data
        del fake_user["id"]
        del fake_user["avatar_picture"]
        return self.api_client.post(reverse(f"users-list"), data=fake_user)
