import graphene
from .card.card_schema import CardSchema
from .deck.deck_schema import DeckSchema
from .whishlist.whishlist_schema import WhishlistSchema
from .mycards.mycards_schema import MyCardSchema
from deck_pocket.models import Card, Deck, Whishlist, MyCards


class Query(graphene.ObjectType):
    all_cards = graphene.List(CardSchema, deck_name=graphene.String())
    card = graphene.List(CardSchema, card_name=graphene.String(), distinct=graphene.Boolean())
    decks = graphene.List(DeckSchema, deck_name=graphene.String())
    whishlist = graphene.List(WhishlistSchema)
    my_cards = graphene.List(MyCardSchema)

    def resolve_all_cards(self, info):
        return Card.objects.all()[:10]

    def resolve_card(self, info, card_name, **kwargs):
        distinct = kwargs.get('distinct')
        queryset = Card.objects.filter(name__icontains=card_name)
        if distinct:
            return queryset.distinct('name')
        return queryset

    def resolve_decks(self, info, **kwargs):
        user = kwargs.pop('user')
        deck_name = kwargs.get('deck_name')
        if deck_name:
            return Deck.objects.filter(name__icontains=deck_name, user_deck=user)
        else:
            return Deck.objects.filter(user_deck=user)

    def resolve_whishlist(self, info, **kwargs):
        user = kwargs.pop('user')
        return Whishlist.objects.filter(user_whishlist=user)

    def resolve_my_cards(self, info, **kwargs):
        user = kwargs.pop('user')
        return MyCards.objects.filter(user_cards=user)
