"""
Authentication Pydantic Schemas

Description:
- This module contains all auth schemas used by API.

"""

from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

from ..constants.auth import JWT_TOKEN_TYPE
from ..core.config import TokenType
from ..schemas.user import UserCreateSchema, UserReadSchema


class RegisterSchema(UserCreateSchema):
    """
    Register Schema

    Description:
    - This schema is used to validate register data passed to API.

    """


class LoginReadSchema(UserReadSchema):
    """
    Login Read Schema

    Description:
    - This schema is used to validate login data returned by API.

    """

    token_type: str = Field(examples=[JWT_TOKEN_TYPE])
    access_token: str = Field(examples=[TokenType.ACCESS_TOKEN])
    refresh_token: str = Field(examples=[TokenType.REFRESH_TOKEN])

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class RegisterReadSchema(LoginReadSchema):
    """
    Register Read Schema

    Description:
    - This schema is used to validate register data returned by API.

    """


class RefreshToken(BaseModel):
    """
    Refresh Token Schema

    Description:
    - This schema is used to validate refresh token passed to API.

    """

    refresh_token: str = Field(examples=[TokenType.REFRESH_TOKEN])

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class RefreshTokenReadSchema(BaseModel):
    """
    Refresh Token Read Schema

    Description:
    - This schema is used to validate refresh token data returned by API.

    """

    token_type: str = Field(examples=[JWT_TOKEN_TYPE])
    access_token: str = Field(examples=[TokenType.ACCESS_TOKEN])

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )
