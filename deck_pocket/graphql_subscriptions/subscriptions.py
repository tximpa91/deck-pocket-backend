import graphene
from graphene_django.types import DjangoObjectType
from graphene_subscriptions.events import CREATED, UPDATED, DELETED
from deck_pocket.graphql_schema.deck.deck_schema import DeckSchema
from deck_pocket.models import Deck
from rx import Observable


class Subscription(graphene.ObjectType):
    deck_created = graphene.Field(DeckSchema)
    deck_updated = graphene.Field(DeckSchema)
    hello = graphene.String()

    def resolve_deck_created(root, info, **kwargs):
        print(root)
        return root.filter(
            lambda event:
            event.operation == CREATED and
            isinstance(event.instance, Deck)
        ).map(lambda event: event.instance)

    def resolve_deck_updated(root, info, id, **kwargs):
        return root.filter(
            lambda event:
                event.operation == UPDATED and
                isinstance(event.instance, Deck) and
                event.instance.pk == int(id)
        ).map(lambda event: event.instance)

    def resolve_hello(root, info, **kwargs):
        try:
            return Observable.interval(1000) \
                .map(lambda i: "hello world!")
        except Exception as error:
            print(str(error))
