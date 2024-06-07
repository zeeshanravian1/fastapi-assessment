"""
User Service

Description:
- This module contains user service.

"""

from typing import Any

from passlib.hash import pbkdf2_sha256
from sqlalchemy.orm import Session

from ..repositories.user import UserRepository
from .base import BaseService


class UserService(BaseService):
    """
    User Service

    Description:
    - This is used to interact with user repository.

    """

    def __init__(self) -> None:
        """
        User Service Constructor

        Description:
        - Initializes user Service object

        """

        super().__init__(UserRepository)

    def create(self, db_session: Session, entity) -> Any:
        """
        Create User

        Description:
        - This method is used to create user.

        Args:
        - `db_session(Session)`: Database session.
        - `entity`: User create schema.

        Returns:
        - Returns created user.

        """

        entity.password = pbkdf2_sha256.hash(entity.password)
        return super().create(db_session, entity)
