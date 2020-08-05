import graphene
from graphene_django.types import DjangoObjectType
from deck_pocket.models import Deck, DefaultDate

GENERIC_SORT_FIELDS = [field.name for field in DefaultDate._meta.get_fields()]
GENERIC_SORT_ORDER = {'asc': '', 'desc': '-'}


class DeckDictionary(graphene.InputObjectType):
    card_id = graphene.String()
    have_it = graphene.Boolean()
    quantity = graphene.Int()


class DeckModifyDictionary(graphene.InputObjectType):
    card_for_deck_id = graphene.String()
    have_it = graphene.Boolean()
    quantity = graphene.Int()
    add = graphene.Boolean()


def first(queryset, limit):
    limit_query = limit.get('first')
    if limit_query:
        return queryset[:limit_query]
    return queryset


def generic_sort(queryset, sort, info=None, default_order=None):
    if sort:
        sort_by_field = sort.get('sort')
        order = sort.get('order')
        if sort_by_field in GENERIC_SORT_FIELDS and order in GENERIC_SORT_ORDER:
            if info:
                info.context.data['sort'] = sort
            return queryset.order_by(f'{GENERIC_SORT_ORDER.get(order, "")}{sort_by_field}')
    elif default_order:
        return queryset.order_by(
            f'{GENERIC_SORT_ORDER[default_order.get("order", "")]}{default_order.get("sort", "")}')
    else:
        return queryset.order_by('-updated')


def wrap_querys(model, query_params):
    return graphene.List(model, first=graphene.Int(), sort=graphene.String(), order=graphene.String(), **query_params)


class DeckQl(DjangoObjectType):
    class Meta:
        model = Deck
