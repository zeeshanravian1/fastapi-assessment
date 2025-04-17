"""User Service Module.

Description:
- This module contains user service.

"""

from fastapi_assessment.apps.base.service import BaseService

from .model import User


class UserService(BaseService[User]):
    """User Service Class.

    :Description:
    - This class provides service for user.

    """
