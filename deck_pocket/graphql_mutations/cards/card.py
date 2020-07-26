from graphene import Mutation, String
from deck_pocket.models import Card, MkmLink
from django.db import transaction
from django.utils import timezone
from graphql import GraphQLError
import logging

logger = logging.getLogger(__name__)


class MkmLinkMutation(Mutation):
    class Input:
        # The input arguments for this mutation
        card_id = String(required=True)

    link = String()

    @transaction.atomic
    def mutate(self, info, card_id, **kwargs):
        try:
            print(__name__)
            logger.info(f"Retrieve MKM link: {card_id}")
            card = Card.objects.get(card_id=card_id)
            mkm_link = MkmLink.objects.filter(card_id=card)
            if mkm_link.count():
                mkm_link = mkm_link[0]
                logger.info(f"Update clicked value, current value: {mkm_link.clicked}")
                mkm_link.clicked = mkm_link.clicked + 1
                mkm_link.updated = timezone.now()
                mkm_link.save()
            else:
                logger.info(f"Add MKM Link : card_id: {card_id}")
                mkm_link = MkmLink(card_id=card, clicked=1)
                mkm_link.save()

            return MkmLinkMutation(link=card.mkm_url)

        except Exception as error:
            logger.error(f"Error trying to update MkmLink with card_id {card_id}")
            raise GraphQLError(str(error))
