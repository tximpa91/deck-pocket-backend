from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.conf import settings
from firebase_admin import auth
from deck_pocket.models import DeckPocketUser


class FireBaseAuth(BasePermission):

    def __init__(self):
        self.firebase_app = settings.FIREBASE_APP
        self.user = None

    def validate_firebase_user(self, headers):
        try:
            if 'Firebase-User' in headers:
                uid = headers.get('Firebase-User')
                logged, user = DeckPocketUser.user_exists(uid)
                if logged:
                    self.user = user
                    return True
                else:
                    user = auth.get_user(uid)
                    logged, user = DeckPocketUser().create_or_login(user.uid)
                    if logged:
                        self.user = user
                    return logged
            return False
        except Exception as error:
            return False

    def has_permission(self, request, view):
        permitted = self.validate_firebase_user(request.headers)
        request.data['user'] = self.user
        return permitted
