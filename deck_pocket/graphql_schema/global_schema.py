import graphene
from .card.card_schema import CardSchema
from .deck.deck_schema import DeckSchema
from .whishlist.whishlist_schema import WhishlistSchema
from .mycards.mycards_schema import MyCardSchema
from deck_pocket.models import Card, Deck, Whishlist, MyCards
from deck_pocket.graphql_fields.custom_fields import first



class Query(graphene.ObjectType):
    all_cards = graphene.List(CardSchema, deck_name=graphene.String(), first=graphene.Int())
    card = graphene.List(CardSchema, card_name=graphene.String(), distinct=graphene.Boolean(), first=graphene.Int())
    decks = graphene.List(DeckSchema, deck_name=graphene.String(), first=graphene.Int())
    whishlist = graphene.Field(WhishlistSchema, first=graphene.Int())
    my_cards = graphene.Field(MyCardSchema, first=graphene.Int())

    def resolve_all_cards(self, info):
        return Card.objects.all()

    def resolve_card(self, info, card_name, **kwargs):
        distinct = kwargs.get('distinct')
        queryset = Card.objects.filter(name__icontains=card_name)
        if distinct:
            queryset = queryset.distinct('name')
        return first(queryset, kwargs)

    def resolve_decks(self, info, **kwargs):
        user = kwargs.pop('user')
        deck_name = kwargs.get('deck_name')
        if deck_name:
            return first(Deck.objects.filter(name__icontains=deck_name, user_deck=user), kwargs)
        else:
            return first(Deck.objects.filter(user_deck=user), kwargs)

    def resolve_whishlist(self, info, **kwargs):
        user = kwargs.pop('user')
        return Whishlist.objects.filter(user_whishlist=user)[0]

    def resolve_my_cards(self, info, **kwargs):
        user = kwargs.pop('user')
        return MyCards.objects.filter(user_cards=user)[0]
