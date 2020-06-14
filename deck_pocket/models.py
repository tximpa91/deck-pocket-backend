from django.db import models
from oauth2_provider.models import AbstractApplication
from django.contrib.postgres.fields import JSONField
from graphql import GraphQLError
from django.utils import timezone
import uuid
from deck_pocket.cardmarket.cardmarket import CardMarketAPI
from django.conf import settings

# Create your models here.


class DefaultDate(models.Model):
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(blank=True, null=True, db_column='updated')

    class Meta:
        abstract = True


class Oauth2ProviderDeckPocket(AbstractApplication):
    scopes = models.CharField(blank=True, null=True, max_length=255)

    def allows_grant_type(self, *grant_types):
        # Assume, for this example, that self.authorization_grant_type is set to self.GRANT_AUTHORIZATION_CODE

        return bool(set([self.authorization_grant_type, self.GRANT_CLIENT_CREDENTIALS, ]) & set(grant_types))

    class Meta:
        verbose_name_plural = "OAuth2 Applications"


class DeckPocketUser(DefaultDate):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uid = models.CharField(max_length=255, db_column='Uid', db_index=True)

    @staticmethod
    def user_exists(uid=None):
        try:
            return True, DeckPocketUser.objects.get(uid=uid)
        except Exception as error:
            return False, None

    @staticmethod
    def create_or_login(uid=None):
        try:
            return True, DeckPocketUser.objects.get_or_create(uid=uid)
        except Exception as error:
            return False, None

    class Meta:
        db_table = 'DeckPocketUser'


class Card(DefaultDate):
    card_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.UUIDField(editable=False, blank=True, null=True)
    oracle_id = models.UUIDField(editable=False, blank=True, null=True)
    name = models.CharField(db_column='name', max_length=255, blank=True, null=True)
    uri = models.URLField(max_length=500, blank=True, null=True)
    scryfall_uri = models.URLField(max_length=500, blank=True, null=True)
    image_uris = JSONField(blank=True, null=True)
    mana_cost = models.CharField(max_length=255, blank=True, null=True)
    cmc = models.IntegerField(blank=True, null=True)
    colors = JSONField(blank=True, null=True)
    type_line = models.CharField(max_length=255, blank=True, null=True)
    color_identity = JSONField(blank=True, null=True)
    reserved = models.BooleanField(default=False, blank=True, null=True)
    nonfoil = models.BooleanField(default=False, blank=True, null=True)
    promo = models.BooleanField(default=False, blank=True, null=True)
    reprint = models.BooleanField(default=False, blank=True, null=True)
    variation = models.BooleanField(default=False, blank=True, null=True)
    set = models.CharField(db_column='set', max_length=255)
    set_name = models.CharField(db_column='set_name', max_length=255, blank=True, null=True)
    set_type = models.CharField(db_column='set_type', max_length=255, blank=True, null=True)
    set_uri = models.URLField(max_length=500, blank=True, null=True)
    set_search_uri = models.URLField(max_length=500, blank=True, null=True)
    scryfall_set_uri = models.URLField(max_length=500, blank=True, null=True)
    rulings_uri = models.URLField(max_length=500, blank=True, null=True)
    prints_search_uri = models.URLField(max_length=500, blank=True, null=True)
    collector_number = models.CharField(max_length=255, blank=True, null=True)
    digital = models.CharField(max_length=255, blank=True, null=True)
    rarity = models.CharField(max_length=255, blank=True, null=True)
    full_art = models.BooleanField(default=False, blank=True, null=True)
    textless = models.BooleanField(default=False, blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True, default=0)
    mkm_url = models.URLField(max_length=2500, blank=True, null=True)

    def update_card(self):
        update = True
        time_now = timezone.now().strftime('%Y-%m-%d')
        if self.updated is None:
            update = True
        elif self.updated.strftime('%Y-%m-%d') != time_now:
            update = True
        if update:
            mkm_info = CardMarketAPI(self.name).get_info()
            if mkm_info:
                self.price = mkm_info['priceGuide']['TREND']
                self.mkm_url = settings.CARD_MARKET_URL + mkm_info['website']
                self.updated = timezone.now()
                self.save()

    @staticmethod
    def get_cards(cards):
        try:
            result = []
            for card in cards:
                card_object = Card.objects.get(card_id=str(card.get('card_id')))
                card_object.update_card()
                result.append({
                    'card': Card.objects.get(card_id=str(card.get('card_id'))), 'have_it': card.get('have_it')})
            return result

        except Card.DoesNotExist:
            raise GraphQLError(f"Card: {card}, doesnt exists")

    class Meta:
        db_table = "DeckPocket_Card"


class Deck(DefaultDate):
    deck_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(db_column='name', max_length=255, blank=True, null=True)
    user_deck = models.ForeignKey('DeckPocketUser', models.CASCADE,
                                  related_name='deck_user', blank=True, null=True, db_column='user_deck')
    deck_type = models.CharField(max_length=255, blank=True, null=True)

    @staticmethod
    def get_deck(deck_id):
        try:
            return Deck.objects.get(deck_id=deck_id)
        except Deck.DoesNotExist:
            raise GraphQLError(f"Deck: {deck_id}, doesnt exists")

    class Meta:
        db_table = "Deck"


class Whishlist(DefaultDate):
    whishlist_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(db_column='name', max_length=255, blank=True, null=True, default='Whishlist')
    user_whishlist = models.ForeignKey('DeckPocketUser', models.CASCADE,
                                       related_name='user_whishlist', blank=True, null=True, db_column='user_whishlist')
    cards = models.ManyToManyField('Card', db_column='cards', related_name='whish_cards', db_table='WhishlistCard')

    class Meta:
        db_table = 'Whishlist'


class MyCards(DefaultDate):
    my_cards_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(db_column='name', max_length=255, blank=True, null=True, default='MyCards')
    user_cards = models.ForeignKey('DeckPocketUser', models.CASCADE,
                                   related_name='user_cards', blank=True, null=True, db_column='user_cards')
    cards = models.ManyToManyField('Card', db_column='cards', related_name='my_cards', db_table='MyCard')

    class Meta:
        db_table = 'MyCards'


class CardForDeck(DefaultDate):
    card_for_deck_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    card = models.ForeignKey('Card', models.CASCADE,
                             related_name='card_for_deck', blank=True, null=True, db_column='card_id')
    deck = models.ForeignKey('Deck', models.CASCADE,
                             related_name='deck_for_card', blank=True, null=True, db_column='deck_id')
    quantity = models.IntegerField(default=1)
    have_it = models.BooleanField(default=False)
    group = models.ForeignKey('GroupCards', models.CASCADE,
                             related_name='group_for_card', blank=True, null=True, db_column='group_id')

    @staticmethod
    def remove_cards(deck):
        CardForDeck.objects.filter(deck=deck).delete()

    class Meta:
        db_table = "CardForDeck"


class GroupCards(DefaultDate):
    group_card_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(db_column='name', max_length=255, blank=True, null=True, default='MyCards')
    deck = models.ForeignKey('Deck', models.CASCADE,
                             related_name='grouped_cards', blank=True, null=True, db_column='deck_id')

    class Meta:
        db_table = "GroupCards"