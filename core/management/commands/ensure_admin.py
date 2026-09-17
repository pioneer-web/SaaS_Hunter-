import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Cria ou atualiza o administrador definido no .env"

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.getenv("ADMIN_USERNAME", "").strip()
        email = os.getenv("ADMIN_EMAIL", "").strip()
        password = os.getenv("ADMIN_PASSWORD", "")

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    "ADMIN_USERNAME ou ADMIN_PASSWORD não configurados. Admin não criado."
                )
            )
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )

        user.email = email or user.email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        action = "criado" if created else "atualizado"
        self.stdout.write(
            self.style.SUCCESS(
                f"Administrador '{username}' {action} com sucesso."
            )
        )
