from graphene_django import DjangoObjectType
from deck_pocket.models import Deck
import graphene


class DeckSchema(DjangoObjectType):
    class Meta:
        model = Deck
