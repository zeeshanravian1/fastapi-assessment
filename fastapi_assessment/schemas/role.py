"""
Role Pydantic Schemas

Description:
- This module contains all role schemas used by API.

"""

from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

from ..constants.role import ROLE_DESCRIPTION, ROLE_NAME
from .base import BaseReadSchema


class RoleBaseSchema(BaseModel):
    """
    Role Base Schema

    Description:
    - This schema is used to validate role base data passed to API.

    """

    role_name: str | None = Field(
        min_length=1,
        max_length=2_55,
        examples=[ROLE_NAME],
    )
    role_description: str | None = Field(
        min_length=1,
        max_length=2_55,
        examples=[ROLE_DESCRIPTION],
    )

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class RoleCreateSchema(RoleBaseSchema):
    """
    Role create Schema

    Description:
    - This schema is used to validate role creation data passed to API.

    """

    role_name: str = Field(
        min_length=1,
        max_length=2_55,
        examples=[ROLE_NAME],
    )


class RoleReadSchema(RoleCreateSchema, BaseReadSchema):
    """
    Role Read Schema

    Description:
    - This schema is used to validate role data returned by API.

    """

    role_name: str = Field(
        min_length=1,
        max_length=2_55,
        examples=[ROLE_NAME],
    )


class RoleUpdateSchema(RoleCreateSchema):
    """
    Role Update Schema

    Description:
    - This schema is used to validate role update data passed to API.

    """
