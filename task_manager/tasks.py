from django.core import mail
from django.template.loader import render_to_string

from task_manager.main.models.task import Task
from task_manager.celery import app


@app.task
def send_assign_notification(task_id: int) -> None:
    task = Task.objects.get(pk=task_id)
    assigned = task.assigned
    send_html_email(
        subject="You've assigned a task.",
        template="notification.html",
        context={"task": task},
        recipients=[assigned.email],
    )


@app.task
def send_html_email(subject: str, template: str, context: dict, recipients: list[str]) -> None:
    html_message = render_to_string(f"emails/{template}", context)
    return mail.send_mail(
        subject=subject,
        message="",
        from_email=None,
        recipient_list=recipients,
        html_message=html_message,
    )
