"""deck_pocket_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import graphene
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from deck_pocket.graphql_schema.global_schema import Query
from deck_pocket.mutations.global_mutations import Mutation
from deck_pocket.custom_auth.auth_middleware import AuthorizationMiddleware
from deck_pocket.auth_ql.oauth_graphql import PrivateGraphQLView

schema = graphene.Schema(query=Query, mutation=Mutation)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('graphql', PrivateGraphQLView.as_view(graphiql=True, schema=schema)),
]
