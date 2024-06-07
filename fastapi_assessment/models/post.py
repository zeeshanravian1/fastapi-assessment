"""
Post Model

Description:
- This file contains model for post table.

"""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.connection import BaseTable
from .user import UserTable


class PostTable(BaseTable):
    """
    Post Table

    Description:
    - This table is used to create post in database.

    """

    text: Mapped[str] = mapped_column(String(2_55))

    # Foreign Keys
    user_id: Mapped[int] = mapped_column(
        ForeignKey(UserTable.id, ondelete="CASCADE")
    )

    # Relationships
    user: Mapped[UserTable] = relationship(
        back_populates="posts", lazy="subquery"
    )
