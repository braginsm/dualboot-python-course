from django.db import models


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
    date_update = models.DateTimeField(auto_now_add=True, blank=True)
    date_deadline = models.DateTimeField(blank=True)
    state = models.CharField(
        max_length=255, default=State.NEW_TASK, choices=State.choices
    )
    priority = models.IntegerField(blank=True)
