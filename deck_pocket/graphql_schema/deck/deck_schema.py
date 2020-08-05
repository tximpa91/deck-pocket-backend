from graphene_django import DjangoObjectType
from deck_pocket.models import Deck, CardForDeck
from deck_pocket.graphql_schema.card_for_deck.cardfordeck import CardForDeckSchema
from deck_pocket.graphql_fields.custom_fields import first, wrap_querys, generic_sort
import graphene


class DeckSchema(DjangoObjectType):
    cards = graphene.List(CardForDeckSchema)

    def resolve_cards(self, info, **kwargs):
        my_cards = info.context.data.get('mycards')
        wishlist = info.context.data.get('wishlist')
        sort = info.context.data.get('sort')
        queryset = CardForDeck.objects.filter(deck=self)
        if my_cards:
            queryset = queryset.filter(have_it=True)
        if wishlist:
            queryset = queryset.filter(have_it=False)

        return generic_sort(queryset=queryset,
                            sort=sort,
                            info=None,
                            default_order={'sort': 'created', 'order': 'desc'})

    class Meta:
        model = Deck
        use_connection = True


