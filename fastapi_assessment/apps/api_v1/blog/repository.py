"""Blog Repository Module.

Description:
- This module contains blog repository.

"""

from fastapi_assessment.apps.base.repository import BaseRepository

from .model import Blog


class BlogRepository(BaseRepository[Blog]):
    """Blog Repository Class.

    :Description:
    - This class provides repository for blog.

    """
