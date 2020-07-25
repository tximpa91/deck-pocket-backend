import graphene
from .card.card_schema import CardSchema
from .deck.deck_schema import DeckSchema
from itertools import chain
from deck_pocket.models import Card, Deck, WishList, MyCards, CardForDeck
from deck_pocket.graphql_fields.custom_fields import first, wrap_querys
from graphql import GraphQLError
from django.core.cache import cache
import logging


class Query(graphene.ObjectType):
    card = wrap_querys(CardSchema, {'card_name': graphene.String(), 'distinct': graphene.Boolean()})
    decks = wrap_querys(DeckSchema, {'deck_name': graphene.String()})
    deck = graphene.Field(DeckSchema, {'deck_id': graphene.String()})
    wish_list = graphene.List(DeckSchema)
    grouped_wish_list = graphene.List(CardSchema)
    my_cards = graphene.List(DeckSchema)
    grouped_my_cards = graphene.List(CardSchema)

    def resolve_all_cards(self, info):
        return Card.objects.all()

    def resolve_card(self, info, card_name, **kwargs):
        result = None
        try:

            distinct = kwargs.get('distinct', 0)
            key = str(distinct) + card_name
            cached_data = cache.get(key)
            print(str(cached_data))
            if cached_data:
                return cached_data
            else:
                queryset = Card.objects.filter(name__icontains=card_name)
                if distinct:
                    queryset = queryset.distinct('name')
                result = first(queryset, kwargs)
            cache.set(key, result)
            return result
        except Exception as error:
            print(str(error))
            return result


    def resolve_decks(self, info, **kwargs):
        user = info.context.data.get('user')
        deck_name = kwargs.get('deck_name')
        if deck_name:
            queryset = first(Deck.objects.filter(name__icontains=deck_name, user_deck=user), kwargs)
        else:
            queryset = first(Deck.objects.filter(user_deck=user), kwargs)
        queryset = queryset.order_by('-updated')
        return queryset

    def resolve_deck(self, info, deck_id, **kwargs):
        try:
            user = info.context.data.get('user')
            return Deck.objects.get(deck_id=deck_id, user_deck=user)
        except Deck.DoesNotExist as error:
            raise GraphQLError(str(error))

    def resolve_wish_list(self, info, **kwargs):
        result = []
        user = info.context.data.get('user')
        info.context.data['wishlist'] = True
        wish_list = WishList.objects.get(user_wish_list=user)
        for deck in wish_list.deck_id.all():
            candidate = deck.deck_for_card.filter(have_it=False)
            if candidate:
                result.append(deck)
        return result

    def resolve_grouped_wish_list(self, info, **kwargs):
        user = info.context.data.get('user')
        whish_list = WishList.objects.get(user_wish_list=user)
        cards_by_decks = []
        for deck in whish_list.deck_id.all():
            candidates_cards = CardForDeck.objects.filter(deck=deck, have_it=False)
            for candidate in candidates_cards:
                if len(Card.get_duplicated(candidate.card.card_id, cards_by_decks)) == 0:
                    cards_by_decks.append(candidate.card)
        return cards_by_decks

    def resolve_my_cards(self, info, **kwargs):
        result = []
        user = info.context.data.get('user')
        info.context.data['mycards'] = True
        my_cards = MyCards.objects.get(user_cards=user)
        for deck in my_cards.deck_id.all():
            candidate = deck.deck_for_card.filter(have_it=True)
            if candidate:
                result.append(deck)
        return result

    def resolve_grouped_my_cards(self, info, **kwargs):
        user = info.context.data.get('user')
        my_cards = MyCards.objects.get(user_cards=user)
        cards_by_decks = []
        for deck in my_cards.deck_id.all():
            candidates_cards = CardForDeck.objects.filter(deck=deck, have_it=True)
            for candidate in candidates_cards:
                print(candidate.card.card_id)
                if len(Card.get_duplicated(candidate.card.card_id, cards_by_decks)) == 0:
                    cards_by_decks.append(candidate.card)
        return cards_by_decks
