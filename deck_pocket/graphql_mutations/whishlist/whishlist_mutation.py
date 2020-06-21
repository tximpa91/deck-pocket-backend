from graphene import Mutation, String, Field, List
from deck_pocket.graphql_schema.whishlist.whishlist_schema import WhishlistSchema
from deck_pocket.models import Whishlist, Card
from django.db import transaction


class CreateOrUpdateWhishList(Mutation):
    class Input:
        # The input arguments for this mutation
        cards = List(String)

    # The class attributes define the response of the mutation
    whishlist = Field(WhishlistSchema)

    @transaction.atomic
    def mutate(self, info, cards, **kwargs):
        """Create or update a whishlist if deck_id is not null if for update"""
        user = kwargs.pop('user')
        whishlist = Whishlist.objects.get_or_create(user_whishlist=user)[0]
        # Associate cards to a Whishlist
        if cards:
            whishlist.cards.clear()
            cards_for_create_or_update = Card.get_cards(cards)
            for card in cards_for_create_or_update:
                whishlist.cards.add(card)
        return CreateOrUpdateWhishList(whishlist=whishlist)
