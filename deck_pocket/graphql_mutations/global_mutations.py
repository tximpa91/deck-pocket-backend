import graphene
from .deck.deck_mutation import CreateOrUpdateDeck, DeleteDeck, AddCardToDeck, DeleteCardToDeck, CreateOrUpdateDeckV2
from .cards.card import MkmLinkMutation


class Mutation(graphene.ObjectType):
    create_or_update_deck = CreateOrUpdateDeck.Field()
    mkm_link = MkmLinkMutation.Field()
    delete_deck = DeleteDeck.Field()
    add_card_to_deck = AddCardToDeck.Field()
    delete_card_to_deck = DeleteCardToDeck.Field()
    create_or_update_deck_v2 = CreateOrUpdateDeckV2.Field()

