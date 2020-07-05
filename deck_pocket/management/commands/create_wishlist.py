from django.core.management.base import BaseCommand, CommandError
from deck_pocket.models import Card, WishList, MyCards, Deck
import traceback
import json
import random
import decimal
from django.db.models import Q


class Command(BaseCommand):

    def handle(self, *args, **options):
        decks = Deck.objects.all()
        WishList.objects.all().delete()
        for deck in decks:
            wish_list = WishList.get_or_create(deck.user_deck)
            wish_list.deck_id.add(deck)
            wish_list.save()
