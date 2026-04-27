from django.core.cache import cache
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


ACCESS_TOKEN_BLACKLIST_PREFIX = "jwt_blacklisted_access:"


def get_blacklisted_access_token_cache_key(jti: str) -> str:
    return f"{ACCESS_TOKEN_BLACKLIST_PREFIX}{jti}"


class BlacklistAwareJWTAuthentication(JWTAuthentication):
    """
    Reject access tokens that were explicitly revoked on logout.
    """

    def get_validated_token(self, raw_token):
        validated_token = super().get_validated_token(raw_token)
        jti = validated_token.get("jti")

        if jti and cache.get(get_blacklisted_access_token_cache_key(jti)):
            raise InvalidToken("Token has been revoked")

        return validated_token
