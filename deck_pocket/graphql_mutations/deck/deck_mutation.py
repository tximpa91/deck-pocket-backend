from graphene import Mutation, String, Field, List
from deck_pocket.graphql_schema.deck.deck_schema import DeckSchema
from deck_pocket.models import Card, Deck, CardForDeck, WishList, MyCards
from django.db import transaction
from deck_pocket.graphql_fields.custom_fields import DeckDictionary
from django.utils import timezone
from graphql import GraphQLError
import logging

logger = logging.getLogger(__name__)


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

            user = info.context.data.get('user')
            deck_id = kwargs.get('deck_id')
            cards = kwargs.get('cards')
            logger.info(f'Create or Update Deck name : {name} , deck_type: {str(deck_type)} , cards: {str(cards)}')
            if deck_id is not None:
                deck = Deck.get_deck(deck_id)
                deck.name = name
                deck.deck_type = deck_type
                deck.updated = timezone.now()
            else:
                deck = Deck(name=name, deck_type=deck_type, user_deck=user, updated=timezone.now())
                wishlist = WishList.get_or_create(user)
                my_cards = MyCards.get_or_create(user)
                wishlist.deck_id.add(deck)
                my_cards.deck_id.add(deck)
            # Associate cards to a deck
            if cards:
                CardForDeck.remove_cards(deck=deck)
                cards_for_create_or_update = Card.get_cards(cards)
                for card in cards_for_create_or_update:
                    CardForDeck(card=card.get('card'), deck=deck,
                                have_it=card.get('have_it'),
                                quantity=card.get('quantity')
                                ).save()

            else:
                if deck_id:
                    CardForDeck.remove_cards(deck=deck)
            deck.save()
            return CreateOrUpdateDeck(deck=deck)
        except Exception as error:
            raise GraphQLError(str(error))


class DeleteDeck(Mutation):
    class Input:
        deck_ids = List(String, required=True)

    message = Field(String)

    @transaction.atomic
    def mutate(self, info, deck_ids, **kwargs):
        try:

            queryset_delete = Deck.objects.filter(deck_id__in=deck_ids)
            queryset_delete.update(deleted=True, updated=timezone.now())
            return DeleteDeck(message=f"Successful deleted Decks: {str(deck_ids)}")
        except Deck.DoesNotExist as error:
            raise GraphQLError(str(error))

