import json
from django.core.management.base import BaseCommand
from post_app.models import PostRaw

class Command(BaseCommand):
    help = 'Load data from a JSON file into the PostRaw model'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='static/json/sample.json')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for entry in data:
                    PostRaw.objects.create(
                        userid=entry['userid'],
                        username=entry['username'],
                        post_time=entry['post_time'],
                        thumbs_up_int=entry['thumbs_up_int'],
                        content=entry['content'],
                        data_type=entry['data_type'],
                        title=entry['title']
                    )
                self.stdout.write(self.style.SUCCESS('Data loaded successfully!'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {e}'))
            # print(f"Attempting to load file from: {file_path}")