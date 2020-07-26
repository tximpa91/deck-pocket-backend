from operator import itemgetter

from fuzzywuzzy import fuzz
from mkmsdk.api_map import _API_MAP
from mkmsdk.mkm import Mkm


class CardMarketAPI(object):

    def __init__(self, card):
        self.mkm = Mkm(_API_MAP["2.0"]["api"], _API_MAP["2.0"]["api_root"])
        self.card = card

    def add_matchstring(self, card):
        card['ratio'] = fuzz.ratio(card.get('enName').lower(), self.card.name.lower())
        card['expansionRatio'] = fuzz.ratio(card.get('expansionName').lower(), self.card.set_name.lower())
        return card

    def filter_response_by_ratio_and_expansion(self, partial_response: list, ratio: int, expansion_ratio: int):
        return list(filter(lambda card: (card.get('ratio') >= ratio and card.get('expansionRatio') >= expansion_ratio),
                           partial_response))

    def clean_response(self, response) -> dict:
        try:
            match_string = list(map(self.add_matchstring, response))
            partial_response = self.filter_response_by_ratio_and_expansion(match_string, 80, 80)
            if not partial_response:
                fixture_match_string = self.filter_response_by_ratio_and_expansion(match_string, 80, 60)
                if fixture_match_string:
                    final_response = sorted(fixture_match_string, key=itemgetter('ratio'), reverse=True)[0]
                else:
                    re_do_matching = sorted(match_string, key=itemgetter('ratio', 'expansionRatio'),
                                            reverse=True)
                    final_response = re_do_matching[0]
            else:
                final_response = sorted(partial_response, key=itemgetter('ratio'), reverse=True)[0]
            return final_response
        except Exception as error:
            return dict

    def get_info(self) -> dict:
        try:
            response_for_card = self.mkm.market_place.find_product(params={"search": self.card.name})
            card_mkm = self.clean_response(response_for_card.json()['product'])
            if card_mkm:
                response_price = self.mkm.market_place.product(product=card_mkm.get('idProduct'))
                return response_price.json()['product']
            return dict
        except Exception as error:
            return dict
