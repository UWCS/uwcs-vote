from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Promotes a user to superuser and staff status"

    def add_arguments(self, parser):
        parser.add_argument(
            "username", type=str, help="The username of the user to promote"
        )

    def handle(self, *args, **options):
        User = get_user_model()
        username = options["username"]

        try:
            user = User.objects.get(username=username)

            if user.is_superuser and user.is_staff:
                self.stdout.write(
                    self.style.WARNING(f"User '{username}' is already a superuser.")
                )
                return

            user.is_staff = True
            user.is_superuser = True
            user.save()

            self.stdout.write(
                self.style.SUCCESS(f"Successfully promoted '{username}' to superuser!")
            )

        except User.DoesNotExist:
            raise CommandError(f"User '{username}' does not exist.")
