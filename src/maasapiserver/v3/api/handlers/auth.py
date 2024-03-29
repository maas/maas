from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from maasapiserver.common.api.base import Handler, handler
from maasapiserver.common.api.models.responses.errors import (
    UnauthorizedBodyResponse,
    ValidationErrorBodyResponse,
)
from maasapiserver.v3.api import services
from maasapiserver.v3.api.models.responses.oauth2 import AccessTokenResponse
from maasapiserver.v3.services import ServiceCollectionV3


class AuthHandler(Handler):
    """Auth API handler."""

    TAGS = ["Auth"]

    TOKEN_TYPE = "bearer"

    @handler(
        path="/auth/login",
        methods=["POST"],
        tags=TAGS,
        responses={
            200: {
                "model": AccessTokenResponse,
            },
            401: {"model": UnauthorizedBodyResponse},
            422: {"model": ValidationErrorBodyResponse},
        },
        response_model_exclude_none=True,
        status_code=200,
    )
    async def login(
        self,
        services: ServiceCollectionV3 = Depends(services),
        form_data: OAuth2PasswordRequestForm = Depends(),
    ) -> AccessTokenResponse:
        token = await services.auth.login(
            form_data.username, form_data.password
        )
        return AccessTokenResponse(
            token_type=self.TOKEN_TYPE, access_token=token.encoded
        )
