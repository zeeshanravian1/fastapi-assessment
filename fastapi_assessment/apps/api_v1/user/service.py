"""User Service Module.

Description:
- This module contains user service.

"""

from collections.abc import Sequence

from fastapi_assessment.apps.base.service import BaseService
from fastapi_assessment.database.session import DBSession

from .helper import get_password_hash
from .model import User, UserCreate


class UserService(BaseService[User]):
    """User Service Class.

    :Description:
    - This class provides service for user.

    """

    async def create(  # type: ignore[override]
        self, db_session: DBSession, record: UserCreate
    ) -> User:
        """Create User.

        :Description:
        - This method creates user.

        :Parameters:
        - `db_session` (DBSession): Database session. **(Required)**
        - `record` (UserCreate): User record. **(Required)**

        :Returns:
        - `record` (User): Created user.

        """
        # Hash password before saving
        record.password = get_password_hash(password=record.password)

        return await super().create(db_session=db_session, record=record)

    async def create_multiple(  # type: ignore[override]
        self, db_session: DBSession, records: list[UserCreate]
    ) -> Sequence[User]:
        """Create Multiple Users.

        :Description:
        - This method creates multiple users.

        :Parameters:
        - `db_session` (DBSession): Database session. **(Required)**
        - `records` (list[UserCreate]): List of user records. **(Required)**

        :Returns:
        - `records` (list[UserCreate]): List of user records.

        """
        # Hash password before saving
        for record in records:
            record.password = get_password_hash(password=record.password)

        return await super().create_multiple(
            db_session=db_session,
            records=records,  # type: ignore[arg-type]
        )
