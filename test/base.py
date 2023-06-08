from http import HTTPStatus
import json
from typing import List, OrderedDict, Union
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from task_manager.main.models.user import User


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    basename: str

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = User.objects.create_superuser(
            "test@test.ru", email=None, password=None, is_staff=True
        )
        cls.client = APIClient()

    @staticmethod
    def create_api_user(self):
        return User.objects.create(**self.user_attributes)

    @staticmethod
    def response_to_list_dict(
        response: List[OrderedDict], map_function=None
    ) -> List[dict]:
        result = []
        for item in response:
            new_element = dict(item)
            result.append(map_function(new_element) if map_function else new_element)
        return result

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.post(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def get_by_id(self, args: List[Union[str, int]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.get(self.detail_url(args))
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def get_list(self, args: List[Union[str, int]] = None) -> List[OrderedDict]:
        self.client.force_login(self.user)
        response = self.client.get(self.list_url(args))
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def put_by_id(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.put(self.detail_url(args), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def patch_by_id(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.patch(self.detail_url(args), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def delete_by_id(
        self, args: List[Union[str, int]] = None, user: User = None
    ) -> bool:
        self.client.force_login(user if user else self.user)
        response = self.client.delete(self.detail_url(args))
        return response.status_code == HTTPStatus.NO_CONTENT
