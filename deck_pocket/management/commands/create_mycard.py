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
        MyCards.objects.all().delete()
        for deck in decks:
            my_cards = MyCards.get_or_create(deck.user_deck)
            my_cards.deck_id.add(deck)
            my_cards.save()
