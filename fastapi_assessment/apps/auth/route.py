"""Authentication Route Module.

Description:
- This module is responsible for handling auth routes.
- It is used to login, refresh token, logout user.

"""

from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_assessment.apps.api_v1.user.model import User
from fastapi_assessment.database.session import DBSession

from .model import (
    LoginResponse,
    RefreshToken,
    RefreshTokenRead,
    RefreshTokenResponse,
)
from .service import AuthenticationService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    path="/login/",
    status_code=status.HTTP_200_OK,
    summary="Perform Authentication",
    response_description="User logged in successfully",
)
async def login(
    db_session: DBSession,
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthenticationService = Depends(
        lambda: AuthenticationService(model=User)
    ),
) -> LoginResponse:
    """Login.

    :Description:
    - This route is used to login user.

    :Args:
    - `email or username` (str): Email or username of user. **(Required)**
    - `password` (str): Password of user. **(Required)**

    :Return:
    - **token_type** (str): Token type of user.
    - **access_token** (str): Access token of user.
    - **refresh_token** (str): Refresh token of user.

    """
    result: LoginResponse = await auth_service.login(
        db_session=db_session,
        form_data=form_data,
    )

    if not isinstance(result, LoginResponse):
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "User not found",
                "data": None,
            },
        )

    return LoginResponse(
        token_type=result.token_type,
        access_token=result.access_token,
        refresh_token=result.refresh_token,
    )


@router.post(
    path="/refresh-token/",
    status_code=status.HTTP_200_OK,
    summary="Refresh Token",
    response_description="Token refreshed successfully",
)
async def refresh_token(
    db_session: DBSession,
    token: RefreshToken,
    auth_service: AuthenticationService = Depends(
        lambda: AuthenticationService(model=User)
    ),
) -> RefreshTokenRead:
    """Refresh Token.

    :Description:
    - This route is used to refresh token.

    :Args:
    - `token` (str): Token to refresh. **(Required)**
    - `db_session` (DBSession): Database session. **(Required)**

    :Return:
    - **token_type** (str): Token type of user.
    - **access_token** (str): Access token of user.

    """
    result: RefreshTokenResponse = await auth_service.refresh_token(
        db_session=db_session,
        token=token.refresh_token,
    )

    if not isinstance(result, RefreshTokenResponse):
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Invalid token",
                "data": None,
            },
        )

    return RefreshTokenRead(
        success=True,
        message="Token refreshed successfully",
        data=RefreshTokenResponse(
            token_type=result.token_type,
            access_token=result.access_token,
        ),
    )
