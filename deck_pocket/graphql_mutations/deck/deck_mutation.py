from graphene import Mutation, String, Field, List
from deck_pocket.graphql_schema.deck.deck_schema import DeckSchema
from deck_pocket.models import Card, Deck, CardForDeck, WishList, MyCards
from django.db import transaction
from deck_pocket.graphql_fields.custom_fields import DeckDictionary, DeckModifyDictionary
from django.utils import timezone
from graphql import GraphQLError
from decimal import Decimal
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


class AddCardToDeck(Mutation):
    class Input:
        # The input arguments for this mutation
        deck_id = String(required=False)
        card = DeckDictionary(required=True)

    deck = Field(DeckSchema)

    @transaction.atomic
    def mutate(self, info, deck_id, card, **kwargs):
        try:
            logger.info(f'Add card to Deck : {deck_id}, card: {str(card)}')
            if deck_id is None:
                raise GraphQLError('DeckId is Mandatory Field')
            if card is None:
                raise GraphQLError('Card is Mandatory Field')

            deck = Deck.get_deck(deck_id)
            card_to_add = Card.get_card(card.get('card_id'))
            card_to_add.update_card()
            card_for_deck = deck.deck_for_card.filter(card=card_to_add)
            if card_for_deck.count() == 0:
                deck.total_price = deck.total_price + Decimal((card_to_add.price * int(card.get('quantity'))))
                deck.total_cards = deck.total_cards + int(card.get('quantity'))
                if card.get('have_it'):
                    deck.cards_had = deck.cards_had + int(card.get('quantity'))

                else:
                    deck.cards_needed = deck.cards_needed + int(card.get('quantity'))
                    deck.budget_needed = deck.budget_needed + Decimal(card_to_add.price * int(card.get('quantity')))

                CardForDeck(card=card_to_add, deck=deck,
                            have_it=card.get('have_it'),
                            quantity=card.get('quantity')
                            ).save()
            else:
                card['add'] = True
                deck.add_or_delete_card(card, card_for_deck[0], card_to_add)

            deck.updated = timezone.now()
            deck.save()
            return AddCardToDeck(deck=deck)
        except Exception as error:
            logger.error(str(error))
            raise GraphQLError(str(error))


class ModifyCardToDeck(Mutation):
    class Input:
        # The input arguments for this mutation
        card = DeckModifyDictionary(required=True)

    deck = Field(DeckSchema)

    @transaction.atomic
    def mutate(self, info, card, **kwargs):
        try:
            logger.info(f'card_for_deck: {str(card)}')
            if card is None:
                raise GraphQLError('Card is Mandatory Field')
            card_for_deck = CardForDeck.objects.get(card_for_deck_id=card.get('card_for_deck_id'))
            card_to_add = card_for_deck.card
            card_to_add.update_card()
            deck = card_for_deck.deck
            if card_for_deck.have_it != card.get('have_it'):
                deck.calculate_meta_data(card_for_deck, card.get('have_it'))
            deck.add_or_delete_card(card, card_for_deck, card_to_add)
            card_for_deck.save()
            deck.updated = timezone.now()
            deck.save()
            return ModifyCardToDeck(deck=deck)
        except Exception as error:
            logger.error(str(error))
            raise GraphQLError(str(error))


class DeleteCardToDeck(Mutation):
    class Input:
        # The input arguments for this mutation
        card_for_deck_id = String(required=True)

    deck = Field(DeckSchema)

    @transaction.atomic
    def mutate(self, info, card_for_deck_id, **kwargs):
        try:
            card_for_deck = CardForDeck.objects.get(card_for_deck_id=card_for_deck_id)
            deck = card_for_deck.deck
            deck.total_cards = deck.total_cards - card_for_deck.quantity
            deck.total_price = deck.total_price - Decimal(card_for_deck.quantity * card_for_deck.card.price)
            if card_for_deck.have_it:
                deck.cards_had = deck.cards_had - card_for_deck.quantity
            else:
                deck.cards_needed = deck.cards_needed - card_for_deck.quantity
                deck.budget_needed = deck.budget_needed - Decimal(card_for_deck.quantity * card_for_deck.card.price)
            card_for_deck.delete()
            deck.updated = timezone.now()
            deck.save()
            return DeleteCardToDeck(deck=deck)
        except Exception as error:
            GraphQLError(str(error))


class CreateOrUpdateDeckV2(Mutation):
    class Input:
        # The input arguments for this mutation
        deck_id = String(required=False)
        name = String(required=True)
        deck_type = String(required=True)

    # The class attributes define the response of the mutation
    deck = Field(DeckSchema)

    @transaction.atomic
    def mutate(self, info, name, deck_type, **kwargs):
        """Create or update a deck if deck_id is not null if for update"""
        try:
            deck_id = kwargs.get('deck_id')
            cards = kwargs.get('cards')
            user = info.context.data.get('user')
            logger.info(f'Create or Update Deck name : {name} , deck_type: {str(deck_type)} , cards: {str(cards)}')
            Deck.get_deck_by_name(name, user)
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
            deck.save()
            return CreateOrUpdateDeck(deck=deck)
        except Exception as error:
            raise GraphQLError(str(error))
