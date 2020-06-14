import graphene


class DeckDictionary(graphene.InputObjectType):
    card_id = graphene.String()
    have_it = graphene.Boolean()
    quantity = graphene.Int()


def first(queryset, limit):
    limit_query = limit.get('first')
    if limit_query:
        return queryset[:limit_query]
    else:
        return queryset


def wrap_querys(model, query_params):
    return graphene.List(model, first=graphene.Int(), **query_params)
