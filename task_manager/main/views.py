from typing import cast
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
import django_filters
from task_manager.main.models.tag import Tag
from task_manager.main.models.task import Task
from task_manager.main.models.user import User
from task_manager.main.permissions import DeleteOnlyForStaff
from task_manager.main.serializers import TagSerializer, TaskSerializer, UserSerializer
from task_manager.services.single_resource import (
    SingleResourceMixin,
    SingleResourceUpdateMixin,
)


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("username",)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter


class TagFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Tag
        fields = ("title",)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
    filterset_class = TagFilter
    permission_classes = [DeleteOnlyForStaff, IsAuthenticated]


class TaskFilter(django_filters.FilterSet):
    state = django_filters.CharFilter()
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all())
    assigned = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ("state", "tags", "assigned", "author")


class TaskViewSet(viewsets.ModelViewSet):
    queryset = (
        Task.objects.all()
        .select_related("author", "assigned")
        .prefetch_related("tags")
        .order_by("id")
    )
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    permission_classes = [DeleteOnlyForStaff, IsAuthenticated]


class CurrentUserViewSet(
    SingleResourceMixin, SingleResourceUpdateMixin, viewsets.ModelViewSet
):
    serializer_class = UserSerializer
    queryset = User.objects.order_by("id")

    def get_object(self) -> User:
        return cast(User, self.request.user)
