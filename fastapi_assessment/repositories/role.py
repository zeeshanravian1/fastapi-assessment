"""
Role Repository

Description:
- This module contains role repository.

"""

from ..models.role import RoleTable
from ..schemas.role import RoleCreateSchema, RoleUpdateSchema
from .base import BaseRepository


class RoleRepository(
    BaseRepository[RoleTable, RoleCreateSchema, RoleUpdateSchema]
):
    """
    Role Repository

    Description:
        - This is used to interact with role table.

    """

    def __init__(self) -> None:
        """
        Role Repository Constructor

        Description:
            - This is used to initialize role repository.

        """

        super().__init__(RoleTable)
