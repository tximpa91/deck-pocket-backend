from operator import itemgetter

from fuzzywuzzy import fuzz
from mkmsdk.api_map import _API_MAP
from mkmsdk.mkm import Mkm


class CardMarketAPI(object):

    def __init__(self, name):
        self.mkm = Mkm(_API_MAP["2.0"]["api"], _API_MAP["2.0"]["api_root"])
        self.name = name

    def add_matchstring(self, card):
        card['ratio'] = fuzz.token_set_ratio(card.get('enName').lower(), self.name)
        return card

    def clean_response(self, response) -> dict:
        match_string = list(map(self.add_matchstring, response))
        partial_response = list(filter(lambda card: card.get('ratio') > 80, match_string))
        final_response = sorted(partial_response, key=itemgetter('ratio'), reverse=True)
        return final_response[0] if final_response else None

    def get_price(self) -> object:
        try:
            response_for_card = self.mkm.market_place.find_product(params={"search": self.name})
            card_mkm = self.clean_response(response_for_card.json()['product'])
            response_price = self.mkm.market_place.product(product=card_mkm.get('idProduct'))
            return response_price.json()['product']['priceGuide']['TREND']
        except:
            return 0
