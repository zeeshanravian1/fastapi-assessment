"""
Post Service

Description:
- This module contains post service.

"""

from cachetools import TTLCache, cached

from ..models.post import PostTable
from ..repositories.post import PostRepository
from .base import BaseService

# Define the cache
cache = TTLCache(
    maxsize=1024, ttl=60 * 5
)  # Cache with 1024 items and TTL of 5 minutes (300 seconds)


class PostService(BaseService):
    """
    Post Service

    Description:
    - This is used to interact with post repository.

    """

    def __init__(self) -> None:
        """
        Post Service Constructor

        Description:
        - Initializes post Service object

        """

        super().__init__(PostRepository)

    def _cache_key(self, user_id: int) -> str:
        return f"user_posts_{user_id}"

    @cached(
        cache, key=lambda self, db_session, user_id: self._cache_key(user_id)
    )
    def read_all_by_user_id(self, db_session, user_id: int) -> list[PostTable]:
        """
        Read All By User ID Service

        Description:
        - This is used to get all posts by user id.

        Args:
        - `db_session (Session)`: Database session.
        - `user_id (INT)`: User ID.

        Returns:
        - All posts by user id.

        """

        return self.repository.read_all_by_user_id(db_session, user_id)
