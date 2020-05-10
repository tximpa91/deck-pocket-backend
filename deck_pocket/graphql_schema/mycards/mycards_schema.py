from graphene_django import DjangoObjectType
from deck_pocket.models import MyCards
import graphene


class MyCardSchema(DjangoObjectType):
    class Meta:
        model = MyCards
