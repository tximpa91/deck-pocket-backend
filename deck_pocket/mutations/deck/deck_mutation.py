from graphene import Mutation, String, Field, List
from deck_pocket.graphql_schema.deck.deck_schema import DeckSchema
from deck_pocket.models import Card, Deck, CardForDeck
from django.db import transaction
from deck_pocket.graphql_fields.custom_fields import DeckDictionary
from django.utils import timezone
import traceback


class CreateOrUpdateDeck(Mutation):
    class Input:
        # The input arguments for this mutation
        deck_id = String(required=False)
        name = String(required=True)
        deck_type = String(required=True)
        cards = List(DeckDictionary)

    # The class attributes define the response of the mutation
    deck = Field(DeckSchema)

    @transaction.atomic
    def mutate(self, info, name, deck_type, **kwargs):
        """Create or update a deck if deck_id is not null if for update"""
        try:
            user = kwargs.pop('user')
            deck_id = kwargs.get('deck_id')
            cards = kwargs.get('cards')
            if deck_id is not None:
                deck = Deck.get_deck(deck_id)
                deck.name = name
                deck.deck_type = deck_type
                deck.updated = timezone.now()
                deck.save()
            else:
                deck = Deck(name=name, deck_type=deck_type, user_deck=user, updated=timezone.now())
                deck.save()
            # Associate cards to a deck
            if cards:
                CardForDeck.remove_cards(deck=deck)
                cards_for_create_or_update = Card.get_cards(cards)
                for card in cards_for_create_or_update:
                    CardForDeck(card=card.get('card'), deck=deck, have_it=card.get('have_it')).save()

            return CreateOrUpdateDeck(deck=deck)
        except Exception as error:
            print(traceback.format_exc())


class DeleteDeck(Mutation):
    class Input:
        deck_id = String(required=True)

    message = Field(String)

    @transaction.atomic
    def mutate(self, info, deck_id, **kwargs):
        try:
            deck = Deck.objects.get(deck_id=deck_id)
            deck.deck_for_card.all().delete()
            deck.grouped_cards.all().delete()
            deck.delete()
            return DeleteDeck(message=f"Successful deleted Deck: {deck_id}")
        except Deck.DoesNotExist as error:
            print(traceback.format_exc())

