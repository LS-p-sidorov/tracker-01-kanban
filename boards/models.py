from django.conf import settings
from django.db import models


class Profile(models.Model):
    class Role(models.TextChoices):
        MANAGER = "manager", "Менеджер"
        MEMBER = "member", "Участник"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)

    @property
    def is_manager(self):
        return self.role == self.Role.MANAGER

    def __str__(self):
        return f"{self.user.username} — {self.get_role_display()}"


class Board(models.Model):
    title = models.CharField("Название", max_length=120)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return self.title


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "todo", "К выполнению"
        IN_PROGRESS = "in_progress", "В работе"
        DONE = "done", "Готово"

    title = models.CharField("Название", max_length=150)
    description = models.TextField("Описание", blank=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tasks")
    status = models.CharField("Статус", max_length=15, choices=Status.choices, default=Status.TODO)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def can_be_moved_by(self, user):
        if not user.is_authenticated:
            return False
        profile = getattr(user, "profile", None)
        if profile and profile.is_manager:
            return True
        return self.author_id == user.id

    def __str__(self):
        return self.title
