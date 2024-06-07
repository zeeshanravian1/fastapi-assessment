"""
Auth Repository

Description:
- This module contains auth repository.

"""

from sqlalchemy.orm import Session

from ..models.user import UserTable
from ..schemas.user import UserCreateSchema, UserUpdateSchema
from .base import BaseRepository


class AuthRepository(
    BaseRepository[UserTable, UserCreateSchema, UserUpdateSchema]
):
    """
    User Repository

    Description:
        - This is used to interact with user table.

    """

    def __init__(self) -> None:
        """
        User Repository Constructor

        Description:
        - This is used to initialize user repository.

        """

        super().__init__(UserTable)

    def login(self, db_session: Session, username: str) -> UserTable | None:
        """
        Login Repository

        Description:
        - This is used to get user details by username or email.

        Args:
        - `db_session (Session)`: Database session.
        - `username (STR)`: Username or email.

        Returns:
        - User details.

        """

        return (
            db_session.query(self.model)
            .filter(
                (self.model.username == username)
                | (self.model.email == username)
            )
            .first()
        )
