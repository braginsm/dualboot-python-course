from http import HTTPStatus
from test.factories.action_client import ActionClient
from typing import List, OrderedDict, Union

from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase


class TestViewSetBase(APITestCase):
    action_client: ActionClient
    api_client: APIClient
    basename: str

    @staticmethod
    def response_to_list_dict(response: List[OrderedDict], map_function=None) -> List[dict]:
        result = []
        for item in response:
            new_element = dict(item)
            result.append(map_function(new_element) if map_function else new_element)
        return result

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.api_client = APIClient()
        cls.action_client = ActionClient(cls.api_client)
        cls.action_client.init_user()
        cls.user = cls.action_client.user

    @classmethod
    def detail_url(cls, args: List[str | int]) -> str:
        return reverse(f"{cls.basename}-detail", args=args)

    @classmethod
    def list_url(cls, args: List[Union[str, int]] | None = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def request_create(self, data: dict, args: List[Union[str, int]] | None = None) -> Response:
        url = self.list_url(args)
        if "id" in data.keys():
            del data["id"]
        return self.api_client.post(url, data=data)

    def create(self, data: dict, args: List[Union[str, int]] | None = None) -> dict:
        response = self.request_create(data, args)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def request_retrieve(self, args: List[str | int]) -> Response:
        url = self.detail_url(args)
        return self.api_client.get(url)

    def retrieve(self, args: List[str | int]) -> dict:
        response = self.request_retrieve(args)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def request_list(self, args: List[Union[str, int]] | None = None) -> Response:
        url = self.list_url(args)
        print(url)
        return self.api_client.get(url)

    def list(self, args: List[Union[str, int]] | None = None) -> List[OrderedDict]:
        response = self.request_list(args)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def request_update(self, data: dict, args: str | int) -> Response:
        url = self.detail_url([args])
        return self.api_client.put(url, data=data)

    def update(self, data: dict, args: str | int) -> dict:
        response = self.request_update(data, args)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def request_patch(self, data: dict, args: str | int) -> Response:
        url = self.detail_url([args])
        return self.api_client.patch(url, data=data)

    def patch(self, data: dict, args: str | int) -> dict:
        response = self.request_patch(data, args)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def request_delete(self, args: str | int) -> Response:
        url = self.detail_url([args])
        return self.api_client.delete(url)

    def delete(self, args: str | int) -> bool:
        response = self.request_delete(args)
        return response.status_code == HTTPStatus.NO_CONTENT

    def assert_need_authorized(self) -> None:
        client = APIClient()
        response = client.get(self.list_url())
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def request_single_resource(self, data: dict | None) -> Response:
        return self.api_client.get(self.list_url(), data=data)

    def single_resource(self, data: dict | None = None) -> dict:
        response = self.request_single_resource(data)
        assert response.status_code == HTTPStatus.OK
        return response.data

    def request_patch_single_resource(self, attributes: dict) -> Response:
        url = self.list_url()
        return self.api_client.patch(url, data=attributes)

    def patch_single_resource(self, attributes: dict) -> dict:
        response = self.request_patch_single_resource(attributes)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data
