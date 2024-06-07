"""
Post Repository

Description:
- This module contains post repository.

"""

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
