import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Loading ingredients to DB'

    def handle(self, *args, **options):
        with open('data/ingredients.json', encoding='utf-8') as file:
            ingredients = json.loads(file.read())
            for ingredient in ingredients:
                Ingredient.objects.get_or_create(**ingredient)
        self.stdout.write('The ingredients has been loaded successfully!')
