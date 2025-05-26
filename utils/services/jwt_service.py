from typing import Type

from django.contrib.auth import get_user_model

from rest_framework.generics import get_object_or_404

from rest_framework_simplejwt.tokens import BlacklistMixin, Token

from utils.enums.action_token_enum import ActionEnum
from utils.exceptions.jwt_exception import JWTException

from apps.employee.models import Employee as User

UserModel: User = get_user_model()

ActionTokenClassType = Type[BlacklistMixin | Token]


class ActionToken(BlacklistMixin, Token):
    """Base token class with blacklist support."""
    pass


class ActivateToken(ActionToken):
    """Token for email activation with custom type and expiration."""
    token_type = ActionEnum.ACTIVATE.token_type
    lifetime = ActionEnum.ACTIVATE.exp_time


class JWTService:
    """Service for creating and validating custom JWT tokens."""

    @staticmethod
    def create_token(user, token_class: ActionTokenClassType):
        """Creates a JWT token for the given user."""
        return token_class.for_user(user)

    @staticmethod
    def validate_token(token, token_class: ActionTokenClassType):
        """Validates and blacklists a JWT token."""
        try:
            token_res = token_class(token)
            token_res.check_blacklist()
        except (Exception,):
            raise JWTException

        token_res.blacklist()
        user_id = token_res.payload.get('user_id')
        return get_object_or_404(UserModel, pk=user_id)
