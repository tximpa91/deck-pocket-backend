from django.core.management.base import BaseCommand, CommandError
from deck_pocket.models import Card
import traceback
import json
import random
import decimal
from django.db.models import Q
import requests
import time



class Command(BaseCommand):
    url = 'https://api.scryfall.com/cards/'
    def handle(self, *args, **options):
        try:

            card_to_update = Card.objects.filter(lang__isnull=True)
            self.stdout.write(str(len(card_to_update)))
            for card in card_to_update:
                try:
                    r = requests.get(f"{self.url}{card.id}")
                    payload = r.json()
                    card.lang = payload['lang']
                    card.save()
                    time.sleep(0.10)
                except Exception as error:
                    pass
            self.stdout.write(str(len("done")))

        except Exception as error:
            self.stderr.write(str(error))
            self.stderr.write(traceback.format_exc())



