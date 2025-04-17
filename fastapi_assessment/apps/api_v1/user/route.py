"""User Route Module.

Description:
- This module is responsible for handling user routes.

"""

from collections.abc import Sequence
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import ORJSONResponse

from fastapi_assessment.apps.api_v1.user.service import UserService
from fastapi_assessment.apps.base.model import BasePaginationData, Message
from fastapi_assessment.database.session import DBSession

from .model import (
    User,
    UserBulkPatch,
    UserBulkRead,
    UserBulkUpdate,
    UserCreate,
    UserPaginationData,
    UserPaginationRead,
    UserPatch,
    UserRead,
    UserResponse,
    UserUpdate,
)

router = APIRouter(prefix="/user", tags=["User"])


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    summary="Create a single user",
    response_description="User created successfully",
)
async def create_user(
    db_session: DBSession,
    record: UserCreate,
    user_service: UserService = Depends(lambda: UserService(model=User)),
) -> UserRead:
    """Create a single user.

    :Description:
    - This route is used to create a single user.

    :Args:
    User details to be created with following fields:
    - `first_name` (str): First name of user. **(Required)**
    - `last_name` (str): Last name of user. **(Required)**
    - `username` (str): Username of user. **(Required)**
    - `email` (EmailStr): Email of user. **(Required)**
    - `password` (str): Password of user. **(Required)**
    - `is_active` (bool): Is user active. **(Required)**

    :Returns:
    User details along with following information:
    - `id` (UUID): Id of user.
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `username` (str): Username of user.
    - `email` (EmailStr): Email of user.
    - `is_active` (bool): Is user active.
    - `created_at` (datetime): Datetime of user creation.
    - `updated_at` (datetime): Datetime of user updation.

    """
    result: User = await user_service.create(
        db_session=db_session, record=record
    )

    return UserRead(
        success=True,
        message="User created successfully",
        data=UserResponse.model_validate(obj=result),
    )


@router.post(
    path="/bulk",
    status_code=status.HTTP_201_CREATED,
    summary="Create multiple users",
    response_description="Users created successfully",
)
async def create_users(
    db_session: DBSession,
    records: list[UserCreate],
    user_service: UserService = Depends(lambda: UserService(model=User)),
) -> UserBulkRead:
    """Create multiple users.

    :Description:
    - This route is used to create multiple users.

    :Args:
    List of user details to be created with following fields:
    - `first_name` (str): First name of user. **(Required)**
    - `last_name` (str): Last name of user. **(Required)**
    - `username` (str): Username of user. **(Required)**
    - `email` (EmailStr): Email of user. **(Required)**
    - `password` (str): Password of user. **(Required)**
    - `is_active` (bool): Is user active. **(Required)**

    :Returns:
    List of user details along with following information:
    - `id` (UUID): Id of user.
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `username` (str): Username of user.
    - `email` (EmailStr): Email of user.
    - `is_active` (bool): Is user active.
    - `created_at` (datetime): Datetime of user creation.
    - `updated_at` (datetime): Datetime of user updation.

    """
    results: Sequence[User] = await user_service.create_multiple(
        db_session=db_session,
        records=records,  # type: ignore[arg-type]
    )

    return UserBulkRead(
        success=True,
        message="Users created successfully",
        data=[UserResponse.model_validate(obj=result) for result in results],
    )


@router.get(
    path="/bulk",
    status_code=status.HTTP_200_OK,
    summary="Retrieve multiple users by IDs",
    response_description="Users retrieved successfully",
)
async def read_users_by_ids(
    db_session: DBSession,
    user_ids: Annotated[list[UUID], Query(...)],
    user_service: UserService = Depends(lambda: UserService(model=User)),
) -> UserBulkRead:
    """Retrieve multiple users by IDs.

    :Description:
    - This route is used to retrieve multiple users by their IDs.

    :Args:
    - `user_ids` (list[UUID]): List of user IDs. **(Required)**

    :Returns:
    List of user details along with following information:
    - `id` (UUID): Id of user.
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `username` (str): Username of user.
    - `email` (EmailStr): Email of user.
    - `is_active` (bool): Is user active.
    - `created_at` (datetime): Datetime of user creation.
    - `updated_at` (datetime): Datetime of user updation.

    """
    results: Sequence[User] = await user_service.read_multiple_by_ids(
        db_session=db_session,
        record_ids=user_ids,  # type: ignore[arg-type]
    )

    return UserBulkRead(
        success=True,
        message="Users retrieved successfully",
        data=[UserResponse.model_validate(obj=result) for result in results],
    )


@router.get(
    path="/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Retrieve a single user by ID",
    response_description="User retrieved successfully",
)
async def read_user_by_id(
    db_session: DBSession,
    user_id: Annotated[UUID, "User ID"],
    user_service: UserService = Depends(lambda: UserService(model=User)),
) -> UserRead:
    """Retrieve a single user by ID.

    :Description:
    - This route is used to retrieve a single user by its ID.

    :Args:
    - `user_id` (UUID): ID of user. **(Required)**

    :Returns:
    User details along with following information:
    - `id` (UUID): Id of user.
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `username` (str): Username of user.
    - `email` (EmailStr): Email of user.
    - `is_active` (bool): Is user active.
    - `created_at` (datetime): Datetime of user creation.
    - `updated_at` (datetime): Datetime of user updation.

    """
    result: User | None = await user_service.read_by_id(
        db_session=db_session, record_id=user_id
    )

    if not isinstance(result, User):
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "User not found",
                "data": None,
            },
        )

    return UserRead(
        success=True,
        message="User retrieved successfully",
        data=UserResponse.model_validate(obj=result),
    )


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    summary="Retrieve all users",
    response_description="Users retrieved successfully",
)
async def read_users(
    db_session: DBSession,
    order_by: str | None = None,
    desc: bool = False,
    page: int | None = None,
    limit: int | None = None,
    search_by: str | None = None,
    search_query: str | None = None,
    user_service: UserService = Depends(lambda: UserService(model=User)),
) -> UserPaginationRead:
    """Retrieve all users.

    :Description:
    - This route is used to retrieve all users.

    :Returns:
    List of user details along with following information:
    - `id` (UUID): Id of user.
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `username` (str): Username of user.
    - `email` (EmailStr): Email of user.
    - `is_active` (bool): Is user active.
    - `created_at` (datetime): Datetime of user creation.
    - `updated_at` (datetime): Datetime of user updation.

    """
    results: BasePaginationData[User] = await user_service.read_all(
        db_session=db_session,
        order_by=order_by,
        desc=desc,
        page=page,
        limit=limit,
        search_by=search_by,
        search_query=search_query,
    )

    return UserPaginationRead(
        success=True,
        message="Users retrieved successfully",
        data=UserPaginationData.model_validate(obj=results),
    )


@router.put(
    path="/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update a single user by ID",
    response_description="User updated successfully",
)
async def update_user_by_id(
    db_session: DBSession,
    user_id: Annotated[UUID, "User ID"],
    record: UserUpdate,
    user_service: UserService = Depends(lambda: UserService(model=User)),
) -> UserRead:
    """Update a single user by ID.

    :Description:
    - This route is used to update a single user by its ID.

    :Args:
    - `user_id` (UUID): ID of user. **(Required)**
    User details to be updated with following fields:
    - `first_name` (str): First name of user. **(Required)**
    - `last_name` (str): Last name of user. **(Required)**
    - `username` (str): Username of user. **(Required)**
    - `email` (EmailStr): Email of user. **(Required)**
    - `password` (str): Password of user. **(Required)**
    - `is_active` (bool): Is user active. **(Required)**

    :Returns:
    User details along with following information:
    - `id` (UUID): Id of user.
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `username` (str): Username of user.
    - `email` (EmailStr): Email of user.
    - `is_active` (bool): Is user active.
    - `created_at` (datetime): Datetime of user creation.
    - `updated_at` (datetime): Datetime of user updation.

    """
    result: User | None = await user_service.update_by_id(
        db_session=db_session, record_id=user_id, record=record
    )

    if not isinstance(result, User):
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "User not found",
                "data": None,
            },
        )

    return UserRead(
        success=True,
        message="User updated successfully",
        data=UserResponse.model_validate(obj=result),
    )


@router.put(
    path="/bulk",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update multiple users by IDs",
    response_description="Users updated successfully",
)
async def update_users_by_ids(
    db_session: DBSession,
    records: list[UserBulkUpdate],
    user_service: UserService = Depends(lambda: UserService(model=User)),
) -> UserBulkRead:
    """Update multiple users by IDs.

    :Description:
    - This route is used to update multiple users by their IDs.

    :Args:
    List of user details to be updated with following fields:
    - `id` (UUID): Id of user. **(Required)**
    - `first_name` (str): First name of user. **(Required)**
    - `last_name` (str): Last name of user. **(Required)**
    - `username` (str): Username of user. **(Required)**
    - `email` (EmailStr): Email of user. **(Required)**
    - `password` (str): Password of user. **(Required)**
    - `is_active` (bool): Is user active. **(Required)**

    :Returns:
    List of user details along with following information:
    - `id` (UUID): Id of user.
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `username` (str): Username of user.
    - `email` (EmailStr): Email of user.
    - `is_active` (bool): Is user active.
    - `created_at` (datetime): Datetime of user creation.
    - `updated_at` (datetime): Datetime of user updation.

    """
    results: Sequence[User] = await user_service.update_multiple_by_ids(
        db_session=db_session,
        records=records,  # type: ignore[arg-type]
    )

    return UserBulkRead(
        success=True,
        message="Users updated successfully",
        data=[UserResponse.model_validate(obj=result) for result in results],
    )


@router.patch(
    path="/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Patch a single user by ID",
    response_description="User patched successfully",
)
async def patch_user_by_id(
    db_session: DBSession,
    user_id: Annotated[UUID, "User ID"],
    record: UserPatch,
    user_service: UserService = Depends(lambda: UserService(model=User)),
) -> UserRead:
    """Patch a single user by ID.

    :Description:
    - This route is used to patch a single user by its ID.

    :Args:
    - `user_id` (UUID): ID of user. **(Required)**
    User details to be patched with following fields:
    - `first_name` (str): First name of user. **(Optional)**
    - `last_name` (str): Last name of user. **(Optional)**
    - `username` (str): Username of user. **(Optional)**
    - `email` (EmailStr): Email of user. **(Optional)**
    - `password` (str): Password of user. **(Optional)**
    - `is_active` (bool): Is user active. **(Optional)**

    :Returns:
    User details along with following information:
    - `id` (UUID): Id of user.
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `username` (str): Username of user.
    - `email` (EmailStr): Email of user.
    - `is_active` (bool): Is user active.
    - `created_at` (datetime): Datetime of user creation.
    - `updated_at` (datetime): Datetime of user updation.

    """
    result: User | None = await user_service.update_by_id(
        db_session=db_session, record_id=user_id, record=record
    )

    if not isinstance(result, User):
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "User not found",
                "data": None,
            },
        )

    return UserRead(
        success=True,
        message="User patched successfully",
        data=UserResponse.model_validate(obj=result),
    )


@router.patch(
    path="/bulk",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Patch multiple users by IDs",
    response_description="Users patched successfully",
)
async def patch_users_by_ids(
    db_session: DBSession,
    records: list[UserBulkPatch],
    user_service: UserService = Depends(lambda: UserService(model=User)),
) -> UserBulkRead:
    """Patch multiple users by IDs.

    :Description:
    - This route is used to patch multiple users by their IDs.

    :Args:
    List of user details to be patched with following fields:
    - `id` (UUID): Id of user. **(Required)**
    - `first_name` (str): First name of user. **(Optional)**
    - `last_name` (str): Last name of user. **(Optional)**
    - `username` (str): Username of user. **(Optional)**
    - `email` (EmailStr): Email of user. **(Optional)**
    - `password` (str): Password of user. **(Optional)**
    - `is_active` (bool): Is user active. **(Optional)**

    :Returns:
    List of user details along with following information:
    - `id` (UUID): Id of user.
    - `first_name` (str): First name of user.
    - `last_name` (str): Last name of user.
    - `username` (str): Username of user.
    - `email` (EmailStr): Email of user.
    - `is_active` (bool): Is user active.
    - `created_at` (datetime): Datetime of user creation.
    - `updated_at` (datetime): Datetime of user updation.

    """
    results: Sequence[User] = await user_service.update_multiple_by_ids(
        db_session=db_session,
        records=records,  # type: ignore[arg-type]
    )

    return UserBulkRead(
        success=True,
        message="Users patched successfully",
        data=[UserResponse.model_validate(obj=result) for result in results],
    )


@router.delete(
    path="/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a single user by ID",
    response_description="User deleted successfully",
)
async def delete_user_by_id(
    db_session: DBSession,
    user_id: Annotated[UUID, "User ID"],
    user_service: UserService = Depends(lambda: UserService(model=User)),
) -> None:
    """Delete a single user by ID.

    :Description:
    - This route is used to delete a single user by its ID.

    :Args:
    - `user_id` (UUID): ID of user. **(Required)**

    :Returns:
    - `None`: No content.

    """
    result: Message | None = await user_service.delete_by_id(
        db_session=db_session, record_id=user_id
    )

    if not isinstance(result, Message):
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "User not found",
                "data": None,
            },
        )


@router.delete(
    path="/bulk",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete multiple users by IDs",
    response_description="Users deleted successfully",
)
async def delete_users_by_ids(
    db_session: DBSession,
    user_ids: Annotated[list[UUID], Query(...)],
    user_service: UserService = Depends(lambda: UserService(model=User)),
) -> None:
    """Delete multiple users by IDs.

    :Description:
    - This route is used to delete multiple users by their IDs.

    :Args:
    - `user_ids` (list[UUID]): List of user IDs. **(Required)**

    :Returns:
    - `None`: No content.

    """
    result: Message | None = await user_service.delete_multiple_by_ids(
        db_session=db_session,
        record_ids=user_ids,  # type: ignore[arg-type]
    )

    if not isinstance(result, Message):
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Users not found",
                "data": None,
            },
        )
