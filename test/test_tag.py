from http import HTTPStatus
from test.factories.base import TestViewSetBase
from test.factories.tag_factory import TagFactory

from task_manager.main.serializers import TagSerializer


class TestTagViewSet(TestViewSetBase):
    basename = "tags"
    edit_fields = {"title": "New test tag"}

    @staticmethod
    def expected_details(entity: dict, attributes: dict) -> dict:
        return {"id": entity["id"], **attributes}

    def test_create(self) -> None:
        tag_attributes = TagSerializer(TagFactory.build()).data
        tag = self.create(tag_attributes)
        expected_response = self.expected_details(tag, tag_attributes)

        assert tag == expected_response

    def test_retrieve(self) -> None:
        tag_attributes = TagSerializer(TagFactory.build()).data
        created_tag = self.create(tag_attributes)
        retrieved_tag = self.retrieve([created_tag["id"]])

        assert created_tag == retrieved_tag

    def test_list(self):
        tag_attributes = TagSerializer(TagFactory.build()).data
        tag = self.create(tag_attributes)
        response = self.list()
        tags = self.response_to_list_dict(response)

        assert self.expected_details(tag, tag_attributes) in tags

    def test_update(self):
        tag_attributes = TagSerializer(TagFactory.build()).data
        tag = self.create(tag_attributes)
        new_attributes = {**tag_attributes, **self.edit_fields}
        expected = self.expected_details(tag, new_attributes)
        new_tag = self.update(expected, args=[tag["id"]])

        assert new_tag == expected

    def test_patch(self):
        tag_attributes = TagSerializer(TagFactory.build()).data
        tag = self.create(tag_attributes)
        expected = {**tag, **self.edit_fields}
        new_tag = self.patch(self.edit_fields, tag["id"])

        assert new_tag == expected

    def test_delete(self):
        tag_attributes = TagSerializer(TagFactory.build()).data
        tag = self.create(tag_attributes)
        tag_id = tag["id"]
        self.user.is_staff = True

        assert self.delete(args=[tag_id])
        assert self.request_delete(args=[tag_id]).status_code == HTTPStatus.NOT_FOUND

    def test_delete_without_permission(self):
        tag_attributes = TagSerializer(TagFactory.build()).data
        tag = self.create(tag_attributes)

        assert self.request_delete(args=[tag["id"]]).status_code == HTTPStatus.FORBIDDEN
