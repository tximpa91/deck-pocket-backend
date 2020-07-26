import graphene
from .deck.deck_mutation import CreateOrUpdateDeck, DeleteDeck
from .cards.card import MkmLinkMutation
from .mycards.mycards_mutation import CreateOrUpdateMyCard


class Mutation(graphene.ObjectType):
    create_or_update_deck = CreateOrUpdateDeck.Field()
    mkm_link = MkmLinkMutation.Field()
    delete_deck = DeleteDeck.Field()
