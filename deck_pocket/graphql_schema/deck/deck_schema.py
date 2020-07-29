from graphene_django import DjangoObjectType
from deck_pocket.models import Deck, CardForDeck
from deck_pocket.graphql_schema.card_for_deck.cardfordeck import CardForDeckSchema
import graphene


class DeckSchema(DjangoObjectType):
    cards = graphene.List(CardForDeckSchema)

    def resolve_cards(self, info, **kwargs):
        my_cards = info.context.data.get('mycards')
        wishlist = info.context.data.get('wishlist')
        if my_cards:
            return CardForDeck.objects.filter(deck=self, have_it=True).order_by('created')
        if wishlist:
            return CardForDeck.objects.filter(deck=self, have_it=False).order_by('created')
        return CardForDeck.objects.filter(deck=self).order_by('created')

    class Meta:
        model = Deck
        use_connection = True


