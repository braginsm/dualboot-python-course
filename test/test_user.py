from typing import List, OrderedDict
from task_manager.main.models.user import User
from task_manager.main.serializers import UserSerializer
from test.base import TestViewSetBase


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = {
        "username": "johnsmith",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@test.com",
        "role": User.Roles.DEVELOPER,
    }
    edit_fields = {"email": "johnsmith@test.com", "role": User.Roles.MANAGER}

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {"id": entity["id"], **attributes}

    def test_create(self):
        self.login()
        user = self.create(self.user_attributes)
        expected_response = self.expected_details(user, self.user_attributes)
        assert user == expected_response

    def test_get_by_id(self):
        self.login()
        user = self.create(self.user_attributes)
        user_id = user["id"]
        compare_user = self.get_by_id(user_id)
        assert compare_user == self.expected_details(user, self.user_attributes)

    def test_get_users(self):
        self.login()
        user = self.create(self.user_attributes)
        response = self.get_list()
        users = self.response_to_list_dict(response)
        assert self.expected_details(user, self.user_attributes) in users

    def test_put_user(self):
        self.login()
        user = self.create(self.user_attributes)
        expected = {**user, **self.edit_fields}
        new_user = self.put_by_id(expected, user["id"])
        assert new_user == expected

    def test_patch_user(self):
        self.login()
        user = self.create(self.user_attributes)
        expected = {**user, **self.edit_fields}
        new_user = self.patch_by_id(self.edit_fields, user["id"])
        assert new_user == expected

    def test_delete_user(self):
        self.login()
        user = self.create(self.user_attributes)
        user_id = user["id"]
        assert self.delete_by_id(user_id)
        assert not self.delete_by_id(user_id)
