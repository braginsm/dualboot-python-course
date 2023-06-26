from unittest.mock import patch, MagicMock
from django.core import mail
from django.template.loader import render_to_string
from task_manager.main.models.task import Task
from task_manager.tasks import send_assign_notification
from test.factories.base import TestViewSetBase


class TestSendEmail(TestViewSetBase):
    basename = "tasks"

    @patch.object(mail, "send_mail")
    def test_send_assign_notification(self, fake_sender: MagicMock) -> None:
        assigned = self.action_client.create_user()
        task = self.action_client.create_task(assigned_id=assigned["id"])

        send_assign_notification(task["id"])

        fake_sender.assert_called_once_with(
            subject="You've assigned a task.",
            message="",
            from_email=None,
            recipient_list=[assigned["email"]],
            html_message=render_to_string(
                "emails/notification.html",
                context={"task": Task.objects.get(pk=task["id"])},
            ),
        )
