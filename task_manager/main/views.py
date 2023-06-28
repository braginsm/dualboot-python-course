from http import HTTPStatus
from typing import Any, cast

import django_filters
from django.http import Http404, HttpResponse
from django.urls import reverse
from requests import Request
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from task_manager.main import serializers
from task_manager.main.models.tag import Tag
from task_manager.main.models.task import Task
from task_manager.main.models.user import User
from task_manager.main.permissions import DeleteOnlyForStaff
from task_manager.main.services.async_celery import AsyncJob, JobStatus
from task_manager.main.services.single_resource import SingleResourceMixin, SingleResourceUpdateMixin


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("username",)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = serializers.UserSerializer
    filterset_class = UserFilter


class TagFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Tag
        fields = ("title",)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = serializers.TagSerializer
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
    serializer_class = serializers.TaskSerializer
    filterset_class = TaskFilter
    permission_classes = [DeleteOnlyForStaff, IsAuthenticated]


class CurrentUserViewSet(SingleResourceMixin, SingleResourceUpdateMixin, viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.order_by("id")

    def get_object(self) -> User:
        return cast(User, self.request.user)


class UserTasksViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.order_by("id").select_related("author", "assigned").prefetch_related("tags")
    serializer_class = serializers.TaskSerializer


class TaskTagsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        task_id = self.kwargs["parent_lookup_task_id"]
        return Task.objects.get(pk=task_id).tags.all()


class CountdownJobViewSet(CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.CountdownJobSerializer

    def get_success_headers(self, data: dict) -> dict[str, str]:
        task_id = data["task_id"]
        return {"Location": reverse("jobs-detail", args=[task_id])}


class AsyncJobViewSet(viewsets.GenericViewSet):
    serializer_class = serializers.JobSerializer

    def get_object(self) -> AsyncJob:
        lookup_url_kwargs = self.lookup_url_kwarg or self.lookup_field
        task_id = self.kwargs[lookup_url_kwargs]
        job = AsyncJob.from_id(task_id)
        if job.status == JobStatus.UNKNOWN:
            raise Http404()
        return job

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse:
        instance = self.get_object()
        serializer_data = self.get_serializer(instance).data
        if instance.status == JobStatus.SUCCESS:
            location = self.request.build_absolute_uri(instance.result)
            return Response(
                serializer_data,
                headers={"location": location},
                status=HTTPStatus.CREATED,
            )
        return Response(serializer_data)
