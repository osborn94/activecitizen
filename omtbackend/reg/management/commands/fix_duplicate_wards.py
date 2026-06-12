from django.core.management.base import BaseCommand
from reg.models import Ward, PollingUnit, User

class Command(BaseCommand):
    help = "Fix duplicate Ward entries by name (case-insensitive) and reassign related objects"

    def handle(self, *args, **options):
        seen = {}

        for ward in Ward.objects.all():
            key = ward.name.strip().lower()

            if key not in seen:
                seen[key] = ward
                self.stdout.write(self.style.SUCCESS(f"Keeping: {ward.name}"))
            else:
                original = seen[key]
                self.stdout.write(self.style.WARNING(f"Replacing: {ward.name} -> {original.name}"))

                # Reassign users
                User.objects.filter(ward=ward).update(ward=original)

                # Reassign polling units
                PollingUnit.objects.filter(ward=ward).update(ward=original)

                # Delete duplicate ward
                ward.delete()

        self.stdout.write(self.style.SUCCESS("Duplicate wards cleaned up successfully."))
