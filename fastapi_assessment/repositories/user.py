"""
User Repository

Description:
- This module contains user repository.

"""

from ..models.user import UserTable
from ..schemas.user import UserCreateSchema, UserUpdateSchema
from .base import BaseRepository


class UserRepository(
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
