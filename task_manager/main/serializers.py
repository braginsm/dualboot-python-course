from rest_framework import serializers
from .models.user import User
from .models.task import Task
from .models.tag import Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "role")


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        field = (
            "id",
            "title",
            "description",
            "date_create",
            "date_update",
            "date_deadline",
            "state",
            "priority",
            "author",
            "assigned",
            "tags",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        field = ("id", "title")
