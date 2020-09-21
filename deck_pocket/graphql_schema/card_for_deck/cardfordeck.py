from graphene_django import DjangoObjectType

from deck_pocket.graphql_fields.custom_fields import generic_sort
from deck_pocket.models import CardForDeck, CardTypes
import graphene
import logging

logger = logging.getLogger(__name__)


class CardForDeckSchema(DjangoObjectType):
    class Meta:
        model = CardForDeck


class GroupedCardsByType(graphene.ObjectType):
    creature = graphene.List(CardForDeckSchema)
    artifact = graphene.List(CardForDeckSchema)
    land = graphene.List(CardForDeckSchema)
    enchantment = graphene.List(CardForDeckSchema)
    instant = graphene.List(CardForDeckSchema)
    planeswalker = graphene.List(CardForDeckSchema)
    sorcery = graphene.List(CardForDeckSchema)


def get_filtered_criteria():
    return (
        {
            'type': CardTypes.CREATURE.value,
            'exclusions': ()
        },
        {
            'type': CardTypes.LAND.value,
            'exclusions': ()
        },
        {
            'type': CardTypes.ENCHANTMENT.value,
            'exclusions': (CardTypes.CREATURE.value,)
        },
        {
            'type': CardTypes.ARTIFACT.value,
            'exclusions': (CardTypes.CREATURE.value, CardTypes.LAND.value)
        },
        {
            'type': CardTypes.INSTANT.value,
            'exclusions': ()
        },
        {
            'type': CardTypes.SORCERY.value,
            'exclusions': ()
        },
        {
            'type': CardTypes.PLANESWALKER.value,
            'exclusions': ()
        },

    )


def get_filtered_query(queryset, sort):
    try:
        result = {}
        for element in get_filtered_criteria():
            queryset_for_filter = queryset
            queryset_for_exclude = queryset_for_filter.filter(card__type_line__icontains=element['type'])
            if element['exclusions']:
                for exclusion in element['exclusions']:
                    queryset_for_exclude = queryset_for_exclude.exclude(card__type_line__icontains=exclusion)

            result.update({element['type'].lower(): generic_sort(queryset=queryset_for_exclude, sort=sort,
                                                                 info=None,
                                                                 default_order={'sort': 'created', 'order': 'asc'})})
        return result
    except Exception as error:
        logger.error(str(error))
