"""
Base Read Pydantic Schema

Description:
- This module contains base read schema used by API.

"""

from datetime import datetime

from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

from ..constants.base import CREATED_AT, ID, UPDATED_AT


class BaseReadSchema(BaseModel):
    """
    Base Read Schema

    Description:
    - This schema is used to validate base data returned by API.

    """

    id: int = Field(examples=[ID])
    created_at: datetime = Field(examples=[CREATED_AT])
    updated_at: datetime | None = Field(examples=[UPDATED_AT])

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )
