# # leveltest/management/commands/import_level_questions.py
# import csv
# from django.core.management.base import BaseCommand
# from leveltest.models import LevelQuestion

# class Command(BaseCommand):
#     help = 'Import level questions from CSV file'

#     def add_arguments(self, parser):
#         parser.add_argument('csv_file', type=str)

#     def handle(self, *args, **options):
#         with open(options['csv_file'], encoding='utf-8') as f:
#             reader = csv.DictReader(f)
#             count = 0
#             for row in reader:
#                 LevelQuestion.objects.create(
#                     type=row['type'],
#                     level=row['level'],
#                     question=row['question'],
#                     option_a=row['option_a'],
#                     option_b=row['option_b'],
#                     option_c=row['option_c'],
#                     option_d=row['option_d'],
#                     correct=row['correct'],
#                     audio_url=row.get('audio_url', '')
#                 )
#                 count += 1
#             self.stdout.write(self.style.SUCCESS(f'✅ Imported {count} questions'))
import csv
from django.core.management.base import BaseCommand
from leveltest.models import LevelQuestion
from pathlib import Path

class Command(BaseCommand):
    help = 'Import level test questions from CSV'

    def handle(self, *args, **kwargs):
        path = Path(__file__).resolve().parent.parent.parent / 'data' / 'questions.csv'
        with open(path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                LevelQuestion.objects.create(
                    type=row['type'].strip().lower(),
                    level=row['level'].strip().upper(),
                    question=row['question'].strip(),
                    option_a=row['option_a'].strip(),
                    option_b=row['option_b'].strip(),
                    option_c=row['option_c'].strip(),
                    option_d=row['option_d'].strip(),
                    correct=row['correct'].strip().upper(),
                    audio_url=row.get('audio_url', '').strip()
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'✅ Imported {count} questions'))
