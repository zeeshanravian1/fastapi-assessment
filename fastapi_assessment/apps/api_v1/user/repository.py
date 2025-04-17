"""User Repository Module.

Description:
- This module contains user repository.

"""

from fastapi_assessment.apps.base.repository import BaseRepository

from .model import User


class UserRepository(BaseRepository[User]):
    """User Repository Class.

    :Description:
    - This class provides repository for user.

    """
