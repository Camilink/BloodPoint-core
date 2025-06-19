from django.core.management.base import BaseCommand
from bloodpoint_app.services import AchievementService


class Command(BaseCommand):
    help = 'Initialize achievement definitions in the database'

    def handle(self, *args, **options):
        self.stdout.write('Initializing achievements...')
        AchievementService.initialize_achievements()
        self.stdout.write(
            self.style.SUCCESS('Successfully initialized achievements')
        )
