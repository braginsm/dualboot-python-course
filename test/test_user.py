from http import HTTPStatus
from test.factories.base import TestViewSetBase
from test.factories.user_factory import UserFactory

from task_manager.main.models.user import User
from task_manager.main.serializers import UserSerializer


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    edit_fields = {"email": "johnsmith@test.com", "role": User.Roles.MANAGER}

    @staticmethod
    def expected_details(entity: dict, attributes: dict) -> dict:
        return {
            **attributes,
            "id": entity["id"],
            "avatar_picture": entity["avatar_picture"],
        }

    def test_create(self) -> None:
        user_attributes = UserSerializer(UserFactory.build()).data
        del user_attributes["avatar_picture"]
        user = self.create(user_attributes)
        expected_response = self.expected_details(user, user_attributes)

        assert user == expected_response

    def test_retrieve(self) -> None:
        user_attributes = UserSerializer(UserFactory.build()).data
        del user_attributes["avatar_picture"]
        created_user = self.create(user_attributes)
        retrieved_user = self.retrieve([created_user["id"]])

        assert created_user == retrieved_user

    def test_list(self):
        user_attributes = UserSerializer(UserFactory.build()).data
        del user_attributes["avatar_picture"]
        user = self.create(user_attributes)
        response = self.list()
        users = self.response_to_list_dict(response)

        assert self.expected_details(user, user_attributes) in users

    def test_update(self):
        fake_user = UserFactory.build()
        user_attributes = UserSerializer(fake_user).data
        del user_attributes["avatar_picture"]
        user = self.create(user_attributes)
        new_attributes = {**user_attributes, **self.edit_fields}
        expected = self.expected_details(user, new_attributes)
        new_user = self.update(new_attributes, args=[user["id"]])

        assert new_user == expected

    def test_patch(self):
        user_attributes = UserSerializer(UserFactory.build()).data
        del user_attributes["avatar_picture"]
        user = self.create(user_attributes)
        expected = {**user, **self.edit_fields}
        new_user = self.patch(self.edit_fields, user["id"])

        assert new_user == expected

    def test_delete_user(self):
        user_attributes = UserSerializer(UserFactory.build()).data
        del user_attributes["avatar_picture"]
        user = self.create(user_attributes)
        user_id = user["id"]

        assert self.delete(args=[user_id])
        assert self.request_delete(args=[user_id]).status_code == HTTPStatus.NOT_FOUND
