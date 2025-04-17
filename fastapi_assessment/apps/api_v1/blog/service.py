"""Blog Service Module.

Description:
- This module contains blog service.

"""

from collections.abc import Sequence

from fastapi_assessment.apps.api_v1.user.model import User
from fastapi_assessment.apps.base.service import BaseService
from fastapi_assessment.database.session import DBSession

from .model import Blog, BlogCreate


class BlogService(BaseService[Blog]):
    """Blog Service Class.

    :Description:
    - This class provides service for blog.

    """

    async def create(  # type: ignore[override]  # pylint: disable=W0221
        self, db_session: DBSession, record: BlogCreate, current_user: User
    ) -> Blog:
        """Create Blog.

        :Description:
        - This method creates blog.

        :Parameters:
        - `db_session` (DBSession): Database session. **(Required)**
        - `record` (BlogCreate): Blog record. **(Required)**

        :Returns:
        - `record` (Blog): Created blog.

        """
        # Set author id
        db_record = Blog(
            **record.model_dump(),
            author_id=current_user.id,
        )
        return await super().create(db_session=db_session, record=db_record)

    # pylint: disable=W0221
    async def create_multiple(  # type: ignore[override]
        self,
        db_session: DBSession,
        records: list[BlogCreate],
        current_user: User,
    ) -> Sequence[Blog]:
        """Create Multiple Blogs.

        :Description:
        - This method creates multiple blogs.

        :Parameters:
        - `db_session` (DBSession): Database session. **(Required)**
        - `records` (list[BlogCreate]): List of blog records. **(Required)**
        - `current_user` (User): Current user. **(Required)**

        :Returns:
        - `records` (list[Blog]): List of created blogs.

        """
        # Set author id
        db_records: list[Blog] = [
            Blog(**record.model_dump(), author_id=current_user.id)
            for record in records
        ]

        return await super().create_multiple(
            db_session=db_session,
            records=db_records,  # type: ignore[reportArgumentType]
        )
