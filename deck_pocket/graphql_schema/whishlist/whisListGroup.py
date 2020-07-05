from graphene_django import DjangoObjectType
from deck_pocket.models import Whishlist
from graphene.types.resolver import dict_resolver
from deck_pocket.graphql_schema.deck.deck_schema import DeckSchema
import graphene


class WhishListSchema(graphene.ObjectType):
    whishlist = graphene.List(DeckSchema)
