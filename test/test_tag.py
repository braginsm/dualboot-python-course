from typing import List, OrderedDict
from task_manager.main.models.tag import Tag
from task_manager.main.models.user import User
from task_manager.main.serializers import TagSerializer
from test.base import TestViewSetBase


class TestTagViewSet(TestViewSetBase):
    basename = "tags"
    tag_attributes = {"title": "Test tag"}
    edit_fields = {"title": "New test tag"}

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {"id": entity["id"], **attributes}

    def test_create(self):
        self.login()
        tag = self.create(self.tag_attributes)
        expected_response = self.expected_details(tag, self.tag_attributes)
        assert tag == expected_response

    def test_get_by_id(self):
        self.login()
        tag = self.create(self.tag_attributes)
        tag_id = tag["id"]
        compare_tag = self.get_by_id(tag_id)
        assert compare_tag == self.expected_details(tag, self.tag_attributes)

    def test_get_tags(self):
        self.login()
        tag = self.create(self.tag_attributes)
        response = self.get_list()
        tags = self.response_to_list_dict(response)
        assert self.expected_details(tag, self.tag_attributes) in tags

    def test_put_tag(self):
        self.login()
        tag = self.create(self.tag_attributes)
        expected = {**tag, **self.edit_fields}
        new_tag = self.put_by_id(expected, tag["id"])
        assert new_tag == expected

    def test_patch_tag(self):
        self.login()
        tag = self.create(self.tag_attributes)
        expected = {**tag, **self.edit_fields}
        new_tag = self.patch_by_id(self.edit_fields, tag["id"])
        assert new_tag == expected

    def test_delete_tag(self):
        self.login()
        tag = self.create(self.tag_attributes)
        tag_id = tag["id"]
        assert self.delete_by_id(tag_id)
        assert not self.delete_by_id(tag_id)

    def test_delete_tag_without_permission(self):
        self.login(is_staff=False)
        tag = self.create(self.tag_attributes)
        assert not self.delete_by_id(tag["id"])
