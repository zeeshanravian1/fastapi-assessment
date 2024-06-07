"""
Post Repository

Description:
- This module contains post repository.

"""

from sqlalchemy.orm import Session

from ..models.post import PostTable
from ..schemas.post import PostCreateSchema, PostUpdateSchema
from .base import BaseRepository


class PostRepository(
    BaseRepository[PostTable, PostCreateSchema, PostUpdateSchema]
):
    """
    Post Repository

    Description:
    - This is used to interact with post table.

    """

    def __init__(self) -> None:
        """
        Post Repository Constructor

        Description:
        - This is used to initialize post repository.

        """

        super().__init__(PostTable)

    def read_all_by_user_id(
        self, db_session: Session, user_id: int
    ) -> list[PostTable]:
        """
        Read All By User ID Repository

        Description:
        - This is used to get all posts by user id.

        Args:
        - `db_session (Session)`: Database session.
        - `user_id (INT)`: User ID.

        Returns:
        - All posts by user id.

        """

        return db_session.query(self.model).filter_by(user_id=user_id).all()
