"""
Post Pydantic Schemas

Description:
- This module contains all post schemas used by API.

"""

from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

from ..constants.post import TEXT
from .base import BaseReadSchema


class PostBaseSchema(BaseModel):
    """
    Post Base Schema

    Description:
    - This schema is used to validate post base data passed to API.

    """

    text: str | None = Field(
        min_length=1,
        max_length=2_55,
        examples=[TEXT],
    )

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class PostCreateSchema(PostBaseSchema):
    """
    Post create Schema

    Description:
    - This schema is used to validate post creation data passed to API.

    """

    text: str = Field(
        min_length=1,
        max_length=2_55,
        examples=[TEXT],
    )


class PostReadSchema(PostCreateSchema, BaseReadSchema):
    """
    Post Read Schema

    Description:
    - This schema is used to validate post data returned by API.

    """


class PostUpdateSchema(PostCreateSchema):
    """
    Post Update Schema

    Description:
    - This schema is used to validate post update data passed to API.

    """
