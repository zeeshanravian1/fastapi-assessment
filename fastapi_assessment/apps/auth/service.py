"""Authentication Service Module.

Description:
- This module contains authentication service.

"""

from fastapi.security import OAuth2PasswordRequestForm

from fastapi_assessment.apps.api_v1.user.model import User
from fastapi_assessment.apps.base.service import BaseService
from fastapi_assessment.database.session import DBSession

from .model import LoginResponse, RefreshTokenResponse
from .repository import AuthenticationRepository


class AuthenticationService(BaseService[User]):
    """Authentication Service Class.

    :Description:
    - This class provides service for authentication.

    """

    def __init__(self, model: type[User]) -> None:
        """Initialize AuthenticationService.

        :Description:
        - This method initializes AuthenticationService with model class.

        :Args:
        - `model` (type[User]): SQLModel model class to use. **(Required)**

        :Returns:
        - `None`

        """
        super().__init__(model)
        self.repository = AuthenticationRepository(model=model)

    async def login(
        self,
        db_session: DBSession,
        form_data: OAuth2PasswordRequestForm,
    ) -> LoginResponse:
        """Login User.

        :Description:
        - This method logs in user.

        :Args:
        - `db_session` (DBSession): Database session. **(Required)**
        - `form_data` (OAuth2PasswordRequestForm): Form data. **(Required)**

        :Return:
        - **token_type** (str): Token type of user.
        - **access_token** (str): Access token of user.
        - **refresh_token** (str): Refresh token of user.

        """
        return await self.repository.login(
            db_session=db_session, form_data=form_data
        )

    async def refresh_token(
        self,
        db_session: DBSession,
        token: str,
    ) -> RefreshTokenResponse:
        """Refresh Token.

        :Description:
        - This method refreshes token.

        :Args:
        - `db_session` (DBSession): Database session. **(Required)**
        - `token` (str): Token to refresh. **(Required)**

        :Return:
        - **token_type** (str): Token type of user.
        - **access_token** (str): Access token of user.

        """
        return await self.repository.refresh_token(
            db_session=db_session, token=token
        )
