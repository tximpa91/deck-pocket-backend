import rest_framework
from graphene_django.views import GraphQLView
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rx.core import ObservableBase, AnonymousObservable

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

    def execute_graphql_request(
            self, request, data, query, variables, operation_name, show_graphiql=False
    ):
        target_result = None

        def override_target_result(value):
            nonlocal target_result
            target_result = value

        execution_result = super().execute_graphql_request(request, data, query, variables, operation_name,
                                                           show_graphiql)
        print(execution_result)
        if execution_result:
            if isinstance(execution_result, ObservableBase) or isinstance(execution_result, AnonymousObservable):
                print("entro")
                target = execution_result.subscribe(on_next=lambda value: override_target_result(value))
                target.dispose()
            else:
                return execution_result

        return target_result

    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super(PrivateGraphQLView, cls).as_view(*args, **kwargs)
        view = permission_classes((TokenHasReadWriteScope, FireBaseAuth,))(view)
        view = authentication_classes((OAuth2Authentication,))(view)
        view = api_view(['POST', 'GET'])(view)
        return view
