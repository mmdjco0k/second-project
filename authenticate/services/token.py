from typing import Tuple

from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework_simplejwt.tokens import RefreshToken
class TokenService:
    @classmethod
    def generate(cls, user_obj: User) -> Tuple[str, str]:
        refresh = RefreshToken.for_user(user_obj)

        access = str(refresh.access_token)
        refresh = str(refresh)

        return access, refresh