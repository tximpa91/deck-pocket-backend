import rest_framework
from graphene_django.views import GraphQLView
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from deck_pocket.custom_auth.firebase_permission import FireBaseAuth
from graphql.backend import GraphQLCoreBackend


class GraphQLCustomCoreBackend(GraphQLCoreBackend):
    def __init__(self, executor=None):
        # type: (Optional[Any]) -> None
        super().__init__(executor)
        self.execute_params['allow_subscriptions'] = True


class PrivateGraphQLView(GraphQLView):
    def parse_body(self, request):
        if isinstance(request, rest_framework.request.Request):
            return request.data
        return super(PrivateGraphQLView, self).parse_body(request)

    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super(PrivateGraphQLView, cls).as_view(*args, **kwargs)
        view = permission_classes((TokenHasReadWriteScope, FireBaseAuth,))(view)
        view = authentication_classes((OAuth2Authentication,))(view)
        view = api_view(['POST', 'GET'])(view)
        return view
