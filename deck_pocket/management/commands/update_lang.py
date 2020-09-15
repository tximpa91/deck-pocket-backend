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
            for card in data:
                card_to_update = Card.objects.filter(id=card.get('id'))
                if card_to_update.count() > 0:
                    card_to_update = card_to_update[0]
                    if card_to_update.lang is None:
                        card_to_update.lang = card.get('lang')
                        card_to_update.save()

            self.stdout.write(str(len("done")))

        except Exception as error:
            self.stderr.write(str(error))
            self.stderr.write(traceback.format_exc())



