"""
Role Service

Description:
- This module contains role service.

"""

from ..repositories.role import RoleRepository
from .base import BaseService


class RoleService(BaseService):
    """
    Role Service

    Description:
    - This is used to interact with role repository.

    """

    def __init__(self) -> None:
        """
        Role Service Constructor

        Description:
        - Initializes Role Service object

        """

        super().__init__(RoleRepository)
