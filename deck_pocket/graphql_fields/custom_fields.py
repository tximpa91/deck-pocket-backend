import graphene
from graphene_django.types import DjangoObjectType
from deck_pocket.models import Deck


class DeckDictionary(graphene.InputObjectType):
    card_id = graphene.String()
    have_it = graphene.Boolean()
    quantity = graphene.Int()


class DeckModifyDictionary(graphene.InputObjectType):
    card_for_deck_id = graphene.String()
    have_it = graphene.Boolean()
    quantity = graphene.Int()
    add = graphene.Boolean()



def first(queryset, limit):
    limit_query = limit.get('first')
    if limit_query:
        return queryset[:limit_query]
    else:
        return queryset


def wrap_querys(model, query_params):
    return graphene.List(model, first=graphene.Int(), **query_params)


class DeckQl(DjangoObjectType):
    class Meta:
        model = Deck
