import json

from django.core.management.base import BaseCommand

from recipes.models import Ingridient


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('data/ingredients.json', encoding='utf-8') as file:
            ingredients = json.loads(file.read())
            for ingredient in ingredients:
                Ingridient.objects.get_or_create(**ingredient)
