from graphene_django import DjangoObjectType
from deck_pocket.models import Card, CardTypes, MyCards, WishList, CardForDeck
from graphql import GraphQLError
import graphene


class CardSchema(DjangoObjectType):
    class Meta:
        model = Card


class CardWithGroupSchema(graphene.ObjectType):
    all = graphene.List(CardSchema)
    creature = graphene.List(CardSchema)
    artifact = graphene.List(CardSchema)
    land = graphene.List(CardSchema)
    enchantment = graphene.List(CardSchema)
    instant = graphene.List(CardSchema)
    planeswalker = graphene.List(CardSchema)
    sorcery = graphene.List(CardSchema)


def group_by_type(card, result):
    for card_type in CardTypes:
        if card.card_type == card_type.value:
            result[card_type.value.lower()].append(card)
            break


def init_result():
    return {card_type.value.lower(): [] for card_type in CardTypes}


def get_grouped_cards(user, have_it):
    my_cards = MyCards.objects.get(user_cards=user)
    result = init_result()
    result['all'] = []
    decks = my_cards.deck_id.filter(deleted=False).values_list('deck_id')
    candidates_cards = CardForDeck.objects.filter(deck__in=decks, have_it=have_it).distinct('card_id'). \
        prefetch_related('card')
    result['all'] = [candidate.card for candidate in candidates_cards]
    for card_type in CardTypes:
        result[card_type.value.lower()] = [candidate.card for candidate in candidates_cards.filter(
            card__card_type=card_type.value.lower())]
    return result
