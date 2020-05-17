from graphene_django import DjangoObjectType
from deck_pocket.models import CardForDeck
from graphql import GraphQLError
import graphene


class CardForDeckSchema(DjangoObjectType):
    class Meta:
        model = CardForDeck