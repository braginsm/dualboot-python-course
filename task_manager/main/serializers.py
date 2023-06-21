from django.conf import settings
from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from task_manager.main.validators import FileMaxSizeValidator
from .models.user import User
from .models.task import Task
from .models.tag import Tag


class UserSerializer(serializers.ModelSerializer):
    avatar_picture = serializers.FileField(
        required=False,
        validators=[
            FileMaxSizeValidator(settings.UPLOAD_MAX_SIZES["avatar_picture"]),
            FileExtensionValidator(["jpeg", "jpg", "png"]),
        ],
    )
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "role", "avatar_picture")


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
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
        fields = ("id", "title")
