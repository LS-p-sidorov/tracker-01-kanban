from django.core.management.base import BaseCommand

from boards.models import Board, Profile, Task


class Command(BaseCommand):
    help = "Создаёт демо-пользователей (manager/member), доску и пару задач."

    def handle(self, *args, **options):
        from django.contrib.auth.models import User

        manager, _ = User.objects.get_or_create(username="manager")
        manager.set_password("Demo12345!")
        manager.save()
        Profile.objects.update_or_create(user=manager, defaults={"role": Profile.Role.MANAGER})

        member, _ = User.objects.get_or_create(username="member")
        member.set_password("Demo12345!")
        member.save()
        Profile.objects.update_or_create(user=member, defaults={"role": Profile.Role.MEMBER})

        board, _ = Board.objects.get_or_create(title="Рабочая доска")
        Task.objects.get_or_create(
            board=board, title="Подготовить макет", author=manager,
            defaults={"status": Task.Status.TODO},
        )
        Task.objects.get_or_create(
            board=board, title="Настроить окружение", author=member,
            defaults={"status": Task.Status.IN_PROGRESS},
        )
        Task.objects.get_or_create(
            board=board, title="Регистрация и вход", author=manager,
            defaults={"status": Task.Status.DONE},
        )
        self.stdout.write(self.style.SUCCESS(
            "Демо-данные созданы: manager / Demo12345!, member / Demo12345!"
        ))
