"""
Auth Service

Description:
- This module contains auth service.

"""

from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import pbkdf2_sha256
from sqlalchemy.orm import Session

from ..constants.auth import JWT_TOKEN_TYPE
from ..core.config import TokenType
from ..core.security import create_token
from ..models.user import UserTable
from ..repositories.auth import AuthRepository
from ..response_messages.auth import auth_response_message
from ..schemas.auth import LoginReadSchema, RegisterReadSchema, RegisterSchema
from .base import BaseService


class AuthService(BaseService):
    """
    Auth Service

    Description:
    - This is used to interact with auth repository.

    """

    def __init__(self) -> None:
        """
        Auth Service Constructor

        Description:
        - Initializes auth Service object

        """

        super().__init__(AuthRepository)

    def register(
        self, db_session: Session, record=RegisterSchema
    ) -> RegisterReadSchema:
        """
        Register Service

        Description:
        - This is used to register user.

        Args:
        - `db_session (Session)`: Database session.
        - `form_data (OAuth2PasswordRequestForm)`: Form data.

        Returns:
        - User details.

        """

        record.password = pbkdf2_sha256.hash(record.password)

        user: UserTable = self.repository.create(
            db_session=db_session, entity=record
        )

        data: dict[str, int | str] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }

        access_token: str = create_token(
            data=data, token_type=TokenType.ACCESS_TOKEN
        )

        refresh_token: str = create_token(
            data=data, token_type=TokenType.REFRESH_TOKEN
        )

        return RegisterReadSchema(
            id=user.id,
            name=user.name,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            role_id=user.role_id,
            created_at=user.created_at,
            updated_at=user.updated_at,
            token_type=JWT_TOKEN_TYPE,
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def login(
        self, db_session: Session, form_data: OAuth2PasswordRequestForm
    ) -> LoginReadSchema | dict[str, str]:
        """
        Login Service

        Description:
        - This is used to login user.

        Args:
        - `db_session (Session)`: Database session.
        - `form_data (OAuth2PasswordRequestForm)`: Form data.

        Returns:
        - User details.

        """

        user: UserTable | None = self.repository.login(
            db_session, form_data.username
        )

        if not user:
            return {"detail": auth_response_message.USER_NOT_FOUND}

        if not pbkdf2_sha256.verify(form_data.password, user.password):
            return {"detail": auth_response_message.INCORRECT_PASSWORD}

        # Create JWT token
        data: dict[str, int | str] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }

        access_token: str = create_token(
            data=data, token_type=TokenType.ACCESS_TOKEN
        )

        refresh_token: str = create_token(
            data=data, token_type=TokenType.REFRESH_TOKEN
        )

        return LoginReadSchema(
            id=user.id,
            name=user.name,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            role_id=user.role_id,
            created_at=user.created_at,
            updated_at=user.updated_at,
            token_type=JWT_TOKEN_TYPE,
            access_token=access_token,
            refresh_token=refresh_token,
        )
