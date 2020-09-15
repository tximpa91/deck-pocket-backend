from django.core.management.base import BaseCommand, CommandError
from deck_pocket.models import Card
import traceback
import json
import random
import decimal
from django.db.models import Q


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            json_file = open('/Users/luisparada/Downloads/all-cards-20200914091746.json', 'r')
            data = json.load(json_file)

            cards_pending = Card.objects.filter(lang__isnull=True).values_list('id', flat=True)
            self.stdout.write(str(len(data)))
            filtered_data = [
                card for card in data if card.get('id') in cards_pending
            ]
            self.stdout.write(str(f"filtered data: {len(data)}"))
            for card in filtered_data:
                card_to_update = Card.objects.get(id=card.get('id'))
                card_to_update.lang = card.get('lang')
                card_to_update.save()

            self.stdout.write(str(len("done")))

        except Exception as error:
            self.stderr.write(str(error))
            self.stderr.write(traceback.format_exc())



