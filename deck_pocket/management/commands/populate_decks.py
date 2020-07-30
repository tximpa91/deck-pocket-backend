from django.core.management.base import BaseCommand, CommandError
from deck_pocket.models import Card, Deck, CardForDeck
import traceback
import json
import random
import decimal
from django.db.models import Q
from django.db import transaction
from django.utils import timezone


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        try:
            decks = Deck.objects.all()
            for deck in decks:
                total_price = 0
                cards_needed = 0
                budget_needed = 0
                cards_had = 0
                total_cards = 0
                card_for_deck = deck.deck_for_card.all()
                for card in card_for_deck:
                    total_cards = total_cards + card.quantity
                    total_price = total_price + (card.card.price * card.quantity)
                    if card.have_it:
                        cards_had = cards_had + card.quantity
                    else:
                        cards_needed = cards_needed + card.quantity
                        budget_needed = budget_needed + (card.card.price * card.quantity)
                deck.total_cards = total_cards
                deck.total_price = total_price
                deck.cards_had = cards_had
                deck.cards_needed = cards_needed
                deck.budget_needed = budget_needed
                deck.updated = timezone.now()
                deck.save()



        except Exception as error:
            self.stderr.write(str(error))