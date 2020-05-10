from graphene_django import DjangoObjectType
from deck_pocket.models import Card
from graphql import GraphQLError
import graphene


class CardSchema(DjangoObjectType):
    class Meta:
        model = Card
