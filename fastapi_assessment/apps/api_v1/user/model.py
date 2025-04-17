"""User Model.

Description:
- This module contains user models.

"""

from collections.abc import Sequence

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from fastapi_assessment.apps.base.model import (
    BasePaginationData,
    BasePaginationRead,
    BaseRead,
    BaseUpdate,
)
from fastapi_assessment.database.connection import Base


class UserBase(SQLModel):
    """User Base Model.

    :Description:
    - This class contains common fields for user models.

    :Attributes:
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `username` (str): Username of user.
    - `email` (EmailStr): Email of user.

    """

    first_name: str = Field(
        min_length=1, max_length=255, schema_extra={"examples": ["John"]}
    )
    last_name: str = Field(
        min_length=1, max_length=255, schema_extra={"examples": ["Doe"]}
    )
    username: str = Field(
        min_length=1,
        max_length=255,
        unique=True,
        schema_extra={"examples": ["johndoe"]},
    )
    email: EmailStr = Field(
        min_length=1,
        max_length=255,
        unique=True,
        schema_extra={"examples": ["johndoe@example.com"]},
    )


class User(Base, UserBase, table=True):
    """User Table.

    :Description:
    - This class contains model for user table.

    :Attributes:
    - `id` (UUID): Unique identifier for user.
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `username` (str): Username of user.
    - `email` (EmailStr): Email of user.
    - `password` (str): Password of user.
    - `is_active` (bool): Is user active.
    - `created_at` (datetime): Timestamp when user was created.
    - `updated_at` (datetime): Timestamp when user was last updated.

    """

    password: str = Field(
        min_length=8,
        max_length=255,
        schema_extra={
            "examples": [
                "Password@123",
            ]
        },
    )
    is_active: bool = Field(
        default=True,
        schema_extra={
            "examples": [
                True,
                False,
            ]
        },
    )
    blogs: list["Blog"] = Relationship(  # type: ignore # noqa: F821
        back_populates="author", cascade_delete=True
    )


class UserCreate(UserBase):
    """User Create Model.

    :Description:
    - This class contains model for creating user.
    - Note: is_active is not included as it defaults to True.

    :Attributes:
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `username` (str): Username of user.
    - `email` (EmailStr): Email of user.
    - `password` (str): Password of user.

    """

    password: str = Field(
        min_length=8,
        max_length=255,
        schema_extra={
            "examples": [
                "Password@123",
            ]
        },
    )


class UserResponse(Base, UserBase):
    """User Response Model.

    :Description:
    - This class contains model for returning user data without password.

    :Attributes:
    - `id` (UUID): Unique identifier for user.
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `username` (str): Username of user.
    - `email` (EmailStr): Email of user.
    - `is_active` (bool): Is user active.
    - `created_at` (datetime): Timestamp when user was created.
    - `updated_at` (datetime): Timestamp when user was last updated.

    """

    is_active: bool = Field(
        schema_extra={
            "examples": [
                True,
                False,
            ]
        },
    )


class UserRead(BaseRead[UserResponse]):
    """User Read Model.

    :Description:
    - This class contains model for reading user.

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `data` (UserResponse | None): Data for response.
    - `error` (str | None): Error message if any.

    """

    data: UserResponse | None = Field(default=None)


class UserBulkRead(BaseRead[UserResponse]):
    """User Bulk Read Model.

    :Description:
    - This class contains model for bulk reading user.

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `data` (list[UserResponse]): Data for response.
    - `error` (str | None): Error message if any.

    """

    data: Sequence[UserResponse]  # type: ignore[assignment]


class UserPaginationData(BasePaginationData[UserResponse]):
    """User Pagination Read Model.

    :Description:
    - This class contains model for pagination reading user.

    :Attributes:
    - `page` (int): Current page number.
    - `limit` (int): Number of records per page.
    - `total_pages` (int): Total number of pages.
    - `total_records` (int): Total number of records.
    - `records` (Sequence[UserResponse]): List of records for current page.

    """

    records: Sequence[UserResponse]


class UserPaginationRead(BasePaginationRead[UserResponse]):
    """User Pagination Read Model.

    :Description:
    - This class contains model for pagination reading user.

    :Attributes:
    - `success` (bool): Success status.
    - `message` (str): Message for response.
    - `data` (UserPaginationData | None): Data for response.
    - `error` (str | None): Error message if any.

    """

    data: UserPaginationData  # type: ignore[assignment]


class UserUpdateBase(UserBase):
    """User Update Base Model.

    :Description:
    - Base class for update operations that includes is_active field.

    :Attributes:
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `username` (str): Username of user.
    - `email` (EmailStr): Email of user.
    - `is_active` (bool): Is user active.

    """

    is_active: bool = Field(
        schema_extra={
            "examples": [
                True,
                False,
            ]
        },
    )


class UserUpdate(UserUpdateBase):
    """User Update Model.

    :Description:
    - This class contains model for updating user.

    :Attributes:
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `username` (str): Username of user.
    - `email` (EmailStr): Email of user.
    - `password` (str): Password of user.
    - `is_active` (bool): Is user active.

    """

    password: str = Field(
        min_length=8,
        max_length=255,
        schema_extra={
            "examples": [
                "Password@123",
            ]
        },
    )


class UserBulkUpdate(BaseUpdate[UserResponse], UserUpdate):
    """User Bulk Update Model.

    :Description:
    - This class contains model for bulk updating user.

    :Attributes:
    - `id` (UUID): Unique identifier for user.
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `username` (str): Username of user.
    - `email` (EmailStr): Email of user.
    - `password` (str): Password of user.
    - `is_active` (bool): Is user active.

    """


class UserPatch(SQLModel):
    """User Patch Model.

    :Description:
    - This class contains model for patching user.

    :Attributes:
    - `first_name` (str | None): First name of user.
    - `last_name` (str | None): Last name of user.
    - `username` (str | None): Username of user.
    - `email` (EmailStr | None): Email of user.
    - `password` (str | None): Password of user.
    - `is_active` (bool | None): Is user active.

    """

    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    is_active: bool | None = None


class UserBulkPatch(BaseUpdate[UserResponse], UserPatch):
    """User Bulk Patch Model.

    :Description:
    - This class contains model for bulk patching user.

    :Attributes:
    - `id` (UUID | int): Unique identifier for user.
    - `first_name` (str | None): First name of user.
    - `last_name` (str | None): Last name of user.
    - `username` (str | None): Username of user.
    - `email` (EmailStr | None): Email of user.
    - `password` (str | None): Password of user.
    - `is_active` (bool | None): Is user active.

    """
