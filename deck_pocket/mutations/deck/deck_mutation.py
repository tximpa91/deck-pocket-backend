from graphene import Mutation, String, Field, List
from deck_pocket.graphql_schema.deck.deck_schema import DeckSchema
from deck_pocket.models import Card, Deck
from django.db import transaction



class CreateOrUpdateDeck(Mutation):
    class Input:
        # The input arguments for this mutation
        deck_id = String(required=False)
        name = String(required=True)
        deck_type = String(required=True)
        cards = List(String)

    # The class attributes define the response of the mutation
    deck = Field(DeckSchema)

    @transaction.atomic
    def mutate(self, info, name, deck_type, **kwargs):
        """Create or update a deck if deck_id is not null if for update"""
        user = kwargs.pop('user')
        deck_id = kwargs.get('deck_id')
        cards = kwargs.get('cards')
        if deck_id is not None:
            deck = Deck.get_deck(deck_id)
            deck.name = name
            deck.deck_type = deck_type
            deck.cards.clear()
            deck.save()
        else:
            deck = Deck(name=name, deck_type=deck_type, user_deck=user)
            deck.save()
        # Associate cards to a deck
        if cards:
            cards_for_create_or_update = Card.get_cards(cards)
            for card in cards_for_create_or_update:
                deck.cards.add(card)
        return CreateOrUpdateDeck(deck=deck)
