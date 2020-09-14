from graphene_django import DjangoObjectType
from deck_pocket.models import Deck, CardForDeck, CardTypes
from deck_pocket.graphql_schema.card_for_deck.cardfordeck import CardForDeckSchema, GroupedCardsByType
from deck_pocket.graphql_fields.custom_fields import first, wrap_querys, generic_sort
import copy
import graphene


def filtered_decks(info, self):
    my_cards = info.context.data.get('mycards')
    wishlist = info.context.data.get('wishlist')
    queryset = CardForDeck.objects.filter(deck=self)
    if my_cards:
        queryset = queryset.filter(have_it=True)
    if wishlist:
        queryset = queryset.filter(have_it=False)

    return queryset


class DeckSchema(DjangoObjectType):
    cards = graphene.List(CardForDeckSchema)
    cards_by_type = graphene.Field(GroupedCardsByType)

    def resolve_cards(self, info, **kwargs):
        sort = info.context.data.get('sort')
        queryset = filtered_decks(info, self)
        return generic_sort(queryset=queryset,
                            sort=sort,
                            info=None,
                            default_order={'sort': 'created', 'order': 'asc'})

    def resolve_cards_by_type(self, info, **kwargs):
        result = {}
        for card_type in CardTypes:
            result[card_type.value.lower()] = []

        sort = info.context.data.get('sort')
        queryset = filtered_decks(info, self)
        creature = generic_sort(queryset=queryset.filter(card__type_line__icontains=CardTypes.CREATURE.value),
                                sort=sort,
                                info=None,
                                default_order={'sort': 'created', 'order': 'asc'})
        land = generic_sort(queryset=queryset.filter(card__type_line__icontains=CardTypes.LAND.value),
                            sort=sort,
                            info=None,
                            default_order={'sort': 'created', 'order': 'asc'})

        return {'creature': creature, 'land': land}

    class Meta:
        model = Deck
        use_connection = True
