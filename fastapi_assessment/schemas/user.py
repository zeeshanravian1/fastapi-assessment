"""
User Pydantic Schemas

Description:
- This module contains all user schemas used by API.

"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_settings import SettingsConfigDict

from ..constants.user import EMAIL, NAME, PASSWORD, ROLE_ID, USERNAME
from .base import BaseReadSchema
from .validators import lowercase_email, password_validator, username_validator


class UserBaseSchema(BaseModel):
    """
    User Base Schema

    Description:
    - This schema is used to validate user base data passed to API.

    """

    name: str | None = Field(min_length=1, max_length=2_55, examples=[NAME])
    username: str | None = Field(
        min_length=1, max_length=2_55, examples=[USERNAME]
    )
    email: EmailStr | None = Field(
        min_length=1, max_length=2_55, examples=[EMAIL]
    )
    role_id: int | None = Field(ge=1, examples=[ROLE_ID])

    # Custom Validators
    username_validator = field_validator("username")(username_validator)
    email_validator = field_validator("email")(lowercase_email)

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class UserCreateSchema(UserBaseSchema):
    """
    User create Schema

    Description:
    - This schema is used to validate user creation data passed to API.

    """

    name: str = Field(min_length=1, max_length=2_55, examples=[NAME])
    username: str = Field(min_length=1, max_length=2_55, examples=[USERNAME])
    email: EmailStr = Field(min_length=1, max_length=2_55, examples=[EMAIL])
    password: str = Field(min_length=8, max_length=1_00, examples=[PASSWORD])
    role_id: int = Field(ge=1, examples=[ROLE_ID])

    # Custom Validators
    password_validator = field_validator("password")(password_validator)


class UserReadSchema(UserBaseSchema, BaseReadSchema):
    """
    User Read Schema

    Description:
    - This schema is used to validate user data returned by API.

    """


class UserUpdateSchema(UserBaseSchema):
    """
    User Update Schema

    Description:
    - This schema is used to validate user update data passed to API.

    """

    name: str | None = Field(min_length=1, max_length=2_55, examples=[NAME])
    username: str | None = Field(
        min_length=1, max_length=2_55, examples=[USERNAME]
    )
    email: EmailStr | None = Field(
        min_length=1, max_length=2_55, examples=[EMAIL]
    )
    role_id: int | None = Field(ge=1, examples=[ROLE_ID])
