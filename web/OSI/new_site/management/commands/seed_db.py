from django.core.management.base import BaseCommand, CommandError
from new_site.models import *


class Command(BaseCommand):
    def add_work_types(self):
        work_types=["Сантехник","Электрик","Уборщик"]
        if WorkType.objects.all().exists():
            return
        for work_type in work_types:
            work_type = WorkType(
                name = work_type
            )
            work_type.save()

    def add_stages(self):
        stages=["Обрабатывается","Обработано","Взято","Выполнено"]
        if Stage.objects.all().exists():
            return
        for stage in stages:
            stage = Stage(
                name = stage
            )
            stage.save()

    def add_time_factors(self):
        time_factors=["Срочно", "Несрочно"]
        if TimeFactor.objects.all().exists():
            return
        for time_factor in time_factors:
            time_factor = TimeFactor(
                name = time_factor
            )
            time_factor.save()

    def handle(self, *args, **options):
        self.add_work_types()
        self.add_time_factors()
        self.add_stages()