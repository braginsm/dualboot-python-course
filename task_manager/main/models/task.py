from django.db import models
from .user import User
from .tag import Tag


class Task(models.Model):
    class State(models.TextChoices):
        NEW_TASK = "new_task"
        IN_DEVELOPMENT = "in_development"
        IN_QA = "in_qa"
        IN_CODE_REVIEW = "in_code_review"
        READY_FOR_RELEASE = "ready_for_release"
        RELEASED = "released"
        ARCHIVED = "archived"

    title = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=255)
    date_create = models.DateTimeField(auto_now_add=True, blank=True)
    date_update = models.DateTimeField()
    date_deadline = models.DateTimeField(blank=True)
    state = models.CharField(
        max_length=255, default=State.NEW_TASK, choices=State.choices
    )
    priority = models.IntegerField(blank=True, default=0)
    author = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author')
    assigned = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='assigned')
    tags = models.ManyToManyField(Tag)
