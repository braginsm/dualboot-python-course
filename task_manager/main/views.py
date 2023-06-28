from http import HTTPStatus
from typing import cast

import django_filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from task_manager.main.models.tag import Tag
from task_manager.main.models.task import Task
from task_manager.main.models.user import User
from task_manager.main.permissions import DeleteOnlyForStaff
from task_manager.main.serializers import (TagSerializer, TaskSerializer,
                                           UserSerializer)
from task_manager.services.single_resource import (SingleResourceMixin,
                                                   SingleResourceUpdateMixin)


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
    queryset = Task.objects.all().select_related("author", "assigned").prefetch_related("tags").order_by("id")
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    permission_classes = [DeleteOnlyForStaff, IsAuthenticated]


class CurrentUserViewSet(SingleResourceMixin, SingleResourceUpdateMixin, viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.order_by("id")

    def get_object(self) -> User:
        return cast(User, self.request.user)


class UserTasksViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.order_by("id").select_related("author", "assigned").prefetch_related("tags")
    serializer_class = TaskSerializer


class TaskTagsViewSet(TagViewSet):
    serializer_class = TagSerializer

    def get_queryset(self) -> list[Tag]:
        task_id = self.kwargs["parent_lookup_task_id"]
        return Task.objects.get(pk=task_id).tags.all()
    
    def create(self, request, *args, **kwargs) -> Response:
        task_id = kwargs['parent_lookup_task_id']
        tag = Tag.objects.create(title=request.data['title'])
        task = Task.objects.get(pk=task_id)
        task.tags.add(tag)
        task.save()
        return Response(data=TagSerializer(tag).data, status=HTTPStatus.CREATED)
