import graphene


class DeckDictionary(graphene.InputObjectType):
    card_id = graphene.String()
    have_it = graphene.Boolean()


def first(queryset, limit):
    limit_query = limit.get('first')
    if limit_query:
        return queryset[:limit_query]
    else:
        return queryset