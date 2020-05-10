import graphene
from .deck.deck_mutation import CreateOrUpdateDeck
from .mycards.mycards_mutation import CreateOrUpdateMyCard
from .whishlist.whishlist_mutation import CreateOrUpdateWhishList


class Mutation(graphene.ObjectType):
    create_or_update_deck = CreateOrUpdateDeck.Field()
    create_or_update_my_card = CreateOrUpdateMyCard.Field()
    create_or_update_whishlist = CreateOrUpdateWhishList.Field()
