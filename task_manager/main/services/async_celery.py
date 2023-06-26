from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from celery import states
from celery.result import AsyncResult
from django.db import models


class JobStatus(models.TextChoices):
    UNKNOWN = "unknown"
    FAILURE = "failure"
    SUCCESS = "success"
    STARTED = "started"


@dataclass
class AsyncJob:
    task_id: str
    status: str
    errors: dict | None = None
    result: Any = None

    @classmethod
    def from_id(cls, task_id: str) -> AsyncJob:
        task = AsyncResult(task_id)
        if task.status == states.PENDING:
            return cls(task_id, JobStatus.UNKNOWN)
        if task.status == states.FAILURE:
            original_exception = task.result
            errors = {"non_field_errors": [str(original_exception)]}
            return cls(task_id, JobStatus.FAILURE, errors=errors)
        if task.status == states.SUCCESS:
            return cls(task_id, JobStatus.SUCCESS, result=task.result)
        return cls(task_id, JobStatus.STARTED)
