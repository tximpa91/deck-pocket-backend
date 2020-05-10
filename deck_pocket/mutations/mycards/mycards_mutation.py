from graphene import Mutation, String, Field, List
from deck_pocket.graphql_schema.mycards.mycards_schema import MyCardSchema
from deck_pocket.models import MyCards, Card
from django.db import transaction


class CreateOrUpdateMyCard(Mutation):
    class Input:
        # The input arguments for this mutation
        cards = List(String)

    # The class attributes define the response of the mutation
    my_card = Field(MyCardSchema)

    @transaction.atomic
    def mutate(self, info, cards, **kwargs):
        """Create or update a mycard if deck_id is not null if for update"""
        user = kwargs.pop('user')
        mycard = MyCards.objects.get_or_create(user_cards=user)[0]
        # Associate cards to a MyCards
        if cards:
            mycard.cards.clear()
            cards_for_create_or_update = Card.get_cards(cards)
            for card in cards_for_create_or_update:
                mycard.cards.add(card)
        return CreateOrUpdateMyCard(my_card=mycard)
