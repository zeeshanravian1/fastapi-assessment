"""
Post Service

Description:
- This module contains post service.

"""

from ..repositories.post import PostRepository
from .base import BaseService


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
