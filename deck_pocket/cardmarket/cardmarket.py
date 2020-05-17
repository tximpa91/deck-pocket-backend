from mkmsdk.mkm import Mkm
from mkmsdk.api_map import _API_MAP


class CardMarketAPI(object):
    def __init__(self):
        self.mkm = Mkm(_API_MAP["2.0"]["api"], _API_MAP["2.0"]["api_root"])

    def get_card(self):
        pass
