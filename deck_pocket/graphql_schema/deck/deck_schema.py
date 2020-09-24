from graphene_django import DjangoObjectType
from deck_pocket.models import Deck, CardForDeck, CardTypes
from deck_pocket.graphql_schema.card_for_deck.cardfordeck import CardForDeckSchema, GroupedCardsByType, \
    get_filtered_query
from deck_pocket.graphql_fields.custom_fields import generic_sort
from graphql import GraphQLError
import graphene
import logging

logger = logging.getLogger(__name__)


def get_queryset(self):
    return CardForDeck.objects.filter(deck=self)


def filtered_decks(info, self):
    my_cards = info.context.data.get('mycards')
    wishlist = info.context.data.get('wishlist')
    queryset = get_queryset(self)
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
        try:
            sort = info.context.data.get('sort')
            queryset = filtered_decks(info, self)

            return get_filtered_query(queryset, sort)
        except Exception as error:
            logger.error(str(error))
            raise GraphQLError(str(error))

    class Meta:
        model = Deck
        use_connection = True
