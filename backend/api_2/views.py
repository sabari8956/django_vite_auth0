from authlib.integrations.django_oauth2 import ResourceProtector
from django.http import JsonResponse
from . import validator

require_auth = ResourceProtector()
validator = validator.Auth0JWTBearerTokenValidator(
    "sportshunt-dev.eu.auth0.com",
    "https://sportshunt-dev.eu.auth0.com/api/v2/"
)
require_auth.register_token_validator(validator)


def public(request):
    """No access token required to access this route
    """
    response = "Hello from a public endpoint! You don't need to be authenticated to see this."
    return JsonResponse(dict(message=response))


@require_auth(None)
def private(request):
    """A valid access token is required to access this route
    """
    response = "Hello from a private endpoint! You need to be authenticated to see this."

    return JsonResponse(dict(message=response))
