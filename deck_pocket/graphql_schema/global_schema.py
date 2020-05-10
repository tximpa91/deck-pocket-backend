import graphene
from .card.card_schema import CardSchema
from .deck.deck_schema import DeckSchema
from deck_pocket.models import Card, Deck


class Query(graphene.ObjectType):
    all_cards = graphene.List(CardSchema, deck_name=graphene.String())
    card = graphene.List(CardSchema, card_name=graphene.String(), distinct=graphene.Boolean())
    decks = graphene.List(DeckSchema)

    def resolve_all_cards(self, info):
        return Card.objects.all()[:10]

    def resolve_card(self, info, card_name, **kwargs):
        distinct = kwargs.get('distinct')
        queryset = Card.objects.filter(name__icontains=card_name)
        if distinct:
            return queryset.distinct('name')
        return queryset

    def resolve_decks(self, info, deck_name, **kwargs):
        user = kwargs.pop('user')
        return Deck.objects.filter(deck_name__icontains=deck_name, user=user)
