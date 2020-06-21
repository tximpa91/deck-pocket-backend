from django.db.models.signals import post_save
from graphene_subscriptions.signals import post_save_subscription
from deck_pocket.models import Deck


def trigger_graphene_subscriptions(sender, **kwargs):
    print('signals are working')
    post_save_subscription(sender, **kwargs)


post_save.connect(trigger_graphene_subscriptions, sender=Deck, dispatch_uid="deck_post_save")
