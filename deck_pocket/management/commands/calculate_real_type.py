from django.core.management.base import BaseCommand, CommandError
from deck_pocket.models import Card, WishList, MyCards, Deck, CardTypes



class Command(BaseCommand):

    def handle(self, *args, **options):
        artifacts = Card.objects.filter(type_line__icontains=CardTypes.ARTIFACT.value).\
            exclude(type_line__icontains=CardTypes.CREATURE.value). \
            exclude(type_line__icontains=CardTypes.LAND.value)
        enchantment = Card.objects.filter(type_line__icontains=CardTypes.ENCHANTMENT.value).\
            exclude(type_line__icontains=CardTypes.CREATURE.value)
        creature = Card.objects.filter(type_line__icontains=CardTypes.CREATURE.value)
        instant = Card.objects.filter(type_line__icontains=CardTypes.INSTANT.value)
        sorcery = Card.objects.filter(type_line__icontains=CardTypes.SORCERY.value)
        land = Card.objects.filter(type_line__icontains=CardTypes.LAND.value)
        planeswalker = Card.objects.filter(type_line__icontains=CardTypes.PLANESWALKER.value)

        artifacts.update(card_type=CardTypes.ARTIFACT.value)
        enchantment.update(card_type=CardTypes.ENCHANTMENT.value)
        creature.update(card_type=CardTypes.CREATURE.value)
        instant.update(card_type=CardTypes.INSTANT.value)
        sorcery.update(card_type=CardTypes.SORCERY.value)
        land.update(card_type=CardTypes.LAND.value)
        planeswalker.update(card_type=CardTypes.PLANESWALKER.value)
