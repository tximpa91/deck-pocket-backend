import graphene
from .deck.deck_mutation import CreateOrUpdateDeck, DeleteDeck
from .mycards.mycards_mutation import CreateOrUpdateMyCard


class Mutation(graphene.ObjectType):
    create_or_update_deck = CreateOrUpdateDeck.Field()
    delete_deck = DeleteDeck.Field()
