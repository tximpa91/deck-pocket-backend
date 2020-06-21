import graphene
from graphene_django.types import DjangoObjectType
from graphene_subscriptions.events import CREATED, UPDATED, DELETED
from deck_pocket.graphql_schema.deck.deck_schema import DeckSchema
from deck_pocket.models import Deck
from rx import Observable


class DeckCreatedSubscription(graphene.ObjectType):
    deck_created = graphene.Field(DeckSchema)

    def resolve_deck_created(root, info, **kwargs):
        return root.filter(
            lambda event:
            event.operation == CREATED and
            isinstance(event.instance, Deck)
        ).map(lambda event: event.instance)


class DeckUpdatedSubscription(graphene.ObjectType):
    deck_updated = graphene.Field(DeckSchema, {'deck_id': graphene.String()})

    def resolve_deck_updated(root, info, deck_id, **kwargs):
        return root.filter(
            lambda event:
            event.operation == UPDATED and
            isinstance(event.instance, Deck) and
            str(event.instance.deck_id) == deck_id
        ).map(lambda event: event.instance)


class Subscription(DeckUpdatedSubscription):
    hello = graphene.String()

    def resolve_hello(root, info, **kwargs):
        try:
            return Observable.interval(1000) \
                .map(lambda i: "hello world!")
        except Exception as error:
            print(str(error))
