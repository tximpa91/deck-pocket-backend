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
            fields = [field.name for field in Card._meta.get_fields()
                      if field.name != 'card_id' and field.name != 'deck_cards'
                      and field.name != 'whish_cards' and field.name != 'my_cards']

            try:
                json_file = open('/Users/luisparada/Downloads/scryfall-all-cards.json', 'r')
                data = json.load(json_file)
                card = {}
                for data_d in data:
                    for key in fields:
                        # if key == "image_uris" or key == "color_identity":
                        #     self.stdout.write(str(data_d[key]))
                        #     d = json.dumps(data_d[key])
                        #     card[key] = d
                        # else:
                        card[key] = data_d.get(key, None)
                    card['price'] = 0
                    Card(**card).save()

            except Exception as error:
                self.stderr.write(str(error))
                self.stderr.write(traceback.format_exc())

        except Exception as error:
            self.stderr.write(str(error))
            self.stderr.write(traceback.format_exc())


