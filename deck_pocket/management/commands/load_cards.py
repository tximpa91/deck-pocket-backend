from django.core.management.base import BaseCommand, CommandError
from deck_pocket.models import Card
import traceback
import requests
import time


class Command(BaseCommand):
    url = 'https://api.scryfall.com/cards/search?order=set&q=e%3Aznr&unique=prints&include_multilingual=true'

    def handle(self, *args, **options):
        try:
            fields = [field.name for field in Card._meta.get_fields()
                      if field.name != 'card_id' and field.name != 'deck_cards'
                      and field.name != 'whish_cards' and field.name != 'my_cards'
                      and field.name != 'mkm_url' and field.name != 'card_for_deck'
                      and field.name != 'linked_card' and field.name != 'card_type'
                      and field.name != 'created' and field.name != 'updated'

                      ]
            try:
                has_more = True

                while has_more:
                    request = requests.get(url=self.url)
                    time.sleep(0.10)
                    response = request.json()
                    has_more = response['has_more']
                    if response.get('next_page'):
                        self.url = response['next_page']
                    data = response['data']
                    card = {}
                    for data_d in data:
                        if data_d.get('lang') == 'en' or data_d.get('lang') == 'es':
                            for key in fields:
                                # if key == "image_uris" or key == "color_identity":
                                #     self.stdout.write(str(data_d[key]))
                                #     d = json.dumps(data_d[key])
                                #     card[key] = d
                                # else:
                                card[key] = data_d.get(key, None)
                            card['price'] = 0
                            if card['printed_name'] is None:
                                card['printed_name'] = card['name']
                            Card(**card).save()

                self.stdout.write(str("Done"))

            except Exception as error:
                self.stderr.write(str(error))
                self.stderr.write(traceback.format_exc())

        except Exception as error:
            self.stderr.write(str(error))
            self.stderr.write(traceback.format_exc())
