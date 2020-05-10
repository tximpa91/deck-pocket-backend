from graphene_django import DjangoObjectType
from deck_pocket.models import Whishlist
import graphene


class WhishlistSchema(DjangoObjectType):
    class Meta:
        model = Whishlist
