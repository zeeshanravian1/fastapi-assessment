"""Authentication Repository Module.

Description:
- This module contains authentication repository.

"""

from typing import Any

import jwt
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import col, or_, select
from sqlmodel.sql._expression_select_cls import (
    SelectOfScalar,  # type: ignore[reportPrivateImportUsage]
)

from fastapi_assessment.apps.api_v1.user.helper import verify_password
from fastapi_assessment.apps.api_v1.user.model import User
from fastapi_assessment.apps.base.repository import BaseRepository
from fastapi_assessment.core.config import TokenType, settings
from fastapi_assessment.core.security import create_token
from fastapi_assessment.database.session import DBSession

from .constant import TOKEN_TYPE
from .model import LoginResponse, RefreshTokenResponse


class AuthenticationRepository(BaseRepository[User]):
    """Authentication Repository Class.

    :Description:
    - This class provides repository for authentication.

    """

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

        :Returns:
        - `record` (LoginRead): Login response.

        """
        query: SelectOfScalar[User] = select(self.model).where(
            or_(
                col(column_expression=self.model.username)
                == form_data.username,
                col(column_expression=self.model.email) == form_data.username,
            ),
            col(column_expression=self.model.email) == form_data.username,
        )

        user: User | None = db_session.exec(statement=query).one_or_none()

        if not user:
            raise ValueError("User not found")
        if not user.is_active:
            raise ValueError("User is not active")

        if not verify_password(
            plain_password=form_data.password,
            hashed_password=user.password,
        ):
            raise ValueError("Incorrect password")

        data: dict[str, Any] = {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
        }

        access_token: str = await create_token(
            data=data, token_type=TokenType.ACCESS_TOKEN
        )

        refresh_token: str = await create_token(
            data=data, token_type=TokenType.REFRESH_TOKEN
        )

        return LoginResponse(
            token_type=TOKEN_TYPE,
            access_token=access_token,
            refresh_token=refresh_token,
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
        - `token` (str): Token. **(Required)**

        :Returns:
        - `record` (RefreshTokenResponse): Refresh token response.

        """
        data: dict[str, Any] = jwt.decode(
            jwt=token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        query: SelectOfScalar[User] = select(self.model).where(
            col(column_expression=self.model.id) == data["id"]
        )
        user: User | None = db_session.exec(statement=query).one_or_none()

        if not user:
            raise ValueError("User not found")

        if not user.is_active:
            raise ValueError("User is not active")

        data = {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
        }

        access_token: str = await create_token(
            data=data, token_type=TokenType.ACCESS_TOKEN
        )

        return RefreshTokenResponse(
            token_type=TOKEN_TYPE,
            access_token=access_token,
        )
