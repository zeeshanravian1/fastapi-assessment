"""Blog Model.

Description:
- This module contains blog models.

"""

from collections.abc import Sequence
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from fastapi_assessment.apps.api_v1.user.model import User
from fastapi_assessment.apps.base.model import (
    BasePaginationData,
    BasePaginationRead,
    BaseRead,
    BaseUpdate,
)
from fastapi_assessment.database.connection import Base


class BlogBase(SQLModel):
    """Blog Base Model.

    :Description:
    - This class contains common fields for blog models.

    :Attributes:
    - `title` (str): Title of blog.
    - `content` (str): Content of blog.

    """

    title: str = Field(
        min_length=1,
        max_length=255,
        schema_extra={"examples": ["My First Blog"]},
    )
    content: str = Field(
        min_length=1,
        max_length=10000,
        schema_extra={"examples": ["This is content of my first blog."]},
    )


class Blog(Base, BlogBase, table=True):
    """Blog Table.

    :Description:
    - This class contains model for blog table.

    :Attributes:
    - `id` (UUID): Unique identifier for blog.
    - `title` (str): Title of blog.
    - `content` (str): Content of blog.
    - `author_id` (UUID): Unique identifier for author.
    - `created_at` (datetime): Timestamp when blog was created.
    - `updated_at` (datetime): Timestamp when blog was last updated.

    """

    author_id: UUID = Field(
        foreign_key="user.id",
        schema_extra={
            "examples": [
                "123e4567-e89b-12d3-a456-426614174000",
            ]
        },
        ondelete="CASCADE",
    )
    author: User = Relationship(back_populates="blogs")


class BlogCreate(BlogBase):
    """Blog Create Model.

    :Description:
    - This class contains model for creating blog.

    :Attributes:
    - `title` (str): Title of blog.
    - `content` (str): Content of blog.
    - `author_id` (UUID): Unique identifier for author.

    """


class BlogResponse(Base, BlogBase):
    """Blog Response Model.

    :Description:
    - This class contains model for returning blog data.

    :Attributes:
    - `id` (UUID): Unique identifier for blog.
    - `title` (str): Title of blog.
    - `content` (str): Content of blog.

    """


class BlogRead(BaseRead[BlogResponse]):
    """Blog Read Model.

    :Description:
    - This class contains model for reading blog.

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `data` (BlogResponse | None): Data for response.
    - `error` (str | None): Error message if any.

    """

    data: BlogResponse | None = Field(default=None)


class BlogBulkRead(BaseRead[BlogResponse]):
    """Blog Bulk Read Model.

    :Description:
    - This class contains model for bulk reading blog.

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `data` (list[BlogResponse]): Data for response.
    - `error` (str | None): Error message if any.

    """

    data: Sequence[BlogResponse]  # type: ignore[assignment]


class BlogPaginationData(BasePaginationData[BlogResponse]):
    """Blog Pagination Read Model.

    :Description:
    - This class contains model for pagination reading blog.

    :Attributes:
    - `page` (int): Current page number.
    - `limit` (int): Number of records per page.
    - `total_pages` (int): Total number of pages.
    - `total_records` (int): Total number of records.
    - `records` (Sequence[BlogResponse]): List of records for current page.

    """

    records: Sequence[BlogResponse]


class BlogPaginationRead(BasePaginationRead[BlogResponse]):
    """Blog Pagination Read Model.

    :Description:
    - This class contains model for pagination reading blog.

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `data` (BlogPaginationData | None): Data for response.
    - `error` (str | None): Error message if any.

    """

    data: BlogPaginationData  # type: ignore[assignment]


class BlogUpdate(BlogBase):
    """Blog Update Model.

    :Description:
    - This class contains model for updating blog.

    :Attributes:
    - `title` (str): Title of blog.
    - `content` (str): Content of blog.

    """


class BlogBulkUpdate(BaseUpdate[BlogResponse], BlogUpdate):
    """Blog Bulk Update Model.

    :Description:
    - This class contains model for bulk updating blog.

    :Attributes:
    - `id` (UUID): Unique identifier for blog.
    - `title` (str): Title of blog.
    - `content` (str): Content of blog.

    """


class BlogPatch(SQLModel):
    """Blog Patch Model.

    :Description:
    - This class contains model for patching blog.

    :Attributes:
    - `title` (str | None): Title of blog.
    - `content` (str | None): Content of blog.

    """

    title: str | None = None
    content: str | None = None


class BlogBulkPatch(BaseUpdate[BlogResponse], BlogPatch):
    """Blog Bulk Patch Model.

    :Description:
    - This class contains model for bulk patching blog.

    :Attributes:
    - `id` (UUID | int): Unique identifier for blog.
    - `title` (str | None): Title of blog.
    - `content` (str | None): Content of blog.

    """
