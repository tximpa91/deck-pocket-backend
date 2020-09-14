from graphene_django import DjangoObjectType
from deck_pocket.models import CardForDeck
from graphql import GraphQLError
import graphene


class CardForDeckSchema(DjangoObjectType):
    class Meta:
        model = CardForDeck


class GroupedCardsByType(graphene.ObjectType):
    creature = graphene.List(CardForDeckSchema)
    artifact = graphene.List(CardForDeckSchema)
    land = graphene.List(CardForDeckSchema)
    enchantment = graphene.List(CardForDeckSchema)
    instant = graphene.List(CardForDeckSchema)
    planeswalker = graphene.List(CardForDeckSchema)
    sorcery = graphene.List(CardForDeckSchema)
