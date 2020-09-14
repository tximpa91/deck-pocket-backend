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
            for data_d in data:
                card = Card.objects.filter(id=data_d.get('id'))
                if card.count() > 0:
                    card = card[0]
                    card.lang = data_d.get('lang')
                    card.save()

            self.stdout.write(str("Done"))

        except Exception as error:
            self.stderr.write(str(error))
            self.stderr.write(traceback.format_exc())



