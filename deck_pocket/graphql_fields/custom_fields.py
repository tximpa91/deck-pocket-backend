import graphene


class DeckDictionary(graphene.InputObjectType):
    card_id = graphene.String()
    have_it = graphene.Boolean()
