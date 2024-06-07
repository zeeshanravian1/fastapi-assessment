"""
User Route Module

Description:
- This module is responsible for handling user routes.
- It is used to create, get, update, delete user details.

"""

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from ..database.session import get_session
from ..models.user import UserTable
from ..response_messages.user import user_response_message
from ..schemas.user import UserCreateSchema, UserReadSchema, UserUpdateSchema
from ..services.user import UserService

router = APIRouter(prefix="/user", tags=["User"])


# Create a single user route
@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    summary="Create a single user",
    response_description="User created successfully",
)
async def create_user(
    record: UserCreateSchema,
    db_session: Session = Depends(get_session),
) -> UserReadSchema:
    """
    Create a single user

    Description:
    - This route is used to create a single user.

    Parameter:
    User details to be created with following fields:
    - **name** (STR): Name of user. **(Required)**
    - **username** (STR): Username of user. **(Required)**
    - **email** (STR): Email of user. **(Required)**
    - **password** (STR): Password of user. **(Required)**
    - **role_id** (INT): Role ID of user. **(Required)**

    Return:
    User details along with following information:
    - **id** (INT): Id of user.
    - **name** (STR): Name of user.
    - **username** (STR): Username of user.
    - **email** (STR): Email of user.
    - **role_id** (INT): Role ID of user.
    - **created_at** (DATETIME): Datetime of user creation.
    - **updated_at** (DATETIME): Datetime of user updation.

    """

    result: UserTable = UserService().create(
        db_session=db_session, entity=record
    )

    return UserReadSchema.model_validate(obj=result)


# Get a single user by id route
@router.get(
    path="/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Get a single user by providing id",
    response_description="User details fetched successfully",
)
async def get_user_by_id(
    user_id: int,
    db_session: Session = Depends(get_session),
) -> UserReadSchema:
    """
    Get a single user

    Description:
    - This route is used to get a single user by providing id.

    Parameter:
    - **user_id** (INT): ID of user to be fetched. **(Required)**

    Return:
    Get a single user with following information:
    - **id** (INT): Id of user.
    - **name** (STR): Name of user.
    - **username** (STR): Username of user.
    - **email** (STR): Email of user.
    - **role_id** (INT): Role ID of user.
    - **created_at** (DATETIME): Datetime of user creation.
    - **updated_at** (DATETIME): Datetime of user updation.

    """

    result: UserTable | None = UserService().read_by_id(
        db_session=db_session, entity_id=user_id
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=user_response_message.USER_NOT_FOUND,
        )

    return UserReadSchema.model_validate(obj=result)


# Get all users route
@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    summary="Get all users",
    response_description="All users fetched successfully",
)
async def get_all_users(
    db_session: Session = Depends(get_session),
):
    """
    Get all users

    Description:
    - This route is used to get all users.

    Return:
    Get all users with following information:
    - **id** (INT): Id of user.
    - **name** (STR): Name of user.
    - **username** (STR): Username of user.
    - **email** (STR): Email of user.
    - **role_id** (INT): Role ID of user.
    - **created_at** (DATETIME): Datetime of user creation.
    - **updated_at** (DATETIME): Datetime of user updation.

    """

    result: list[UserTable] = UserService().read_all(db_session=db_session)

    return result


# Update a single user route
@router.put(
    path="/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update a single user by providing id",
    response_description="User updated successfully",
)
async def update_user(
    user_id: int,
    record: UserUpdateSchema,
    db_session: Session = Depends(get_session),
) -> UserReadSchema:
    """
    Update a single user

    Description:
    - This route is used to update a single user by providing id.

    Parameter:
    - **user_id** (INT): ID of user to be updated. **(Required)**
    User details to be updated with following fields:
    - **name** (STR): Name of user. **(Required)**
    - **username** (STR): Username of user. **(Required)**
    - **email** (STR): Email of user. **(Required)**
    - **password** (STR): Password of user. **(Required)**
    - **role_id** (INT): Role ID of user. **(Required)**

    Return:
    User details along with following information:
    - **id** (INT): Id of user.
    - **name** (STR): Name of user.
    - **username** (STR): Username of user.
    - **email** (STR): Email of user.
    - **role_id** (INT): Role ID of user.
    - **created_at** (DATETIME): Datetime of user creation.
    - **updated_at** (DATETIME): Datetime of user updation.

    """

    result: UserTable | None = UserService().update(
        db_session=db_session, entity_id=user_id, entity=record
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=user_response_message.USER_NOT_FOUND,
        )

    return UserReadSchema.model_validate(obj=result)


# Delete a single user route
@router.delete(
    path="/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a single user by providing id",
    response_description="User deleted successfully",
)
async def delete_user(
    user_id: int,
    db_session: Session = Depends(get_session),
) -> None:
    """
    Delete a single user

    Description:
    - This route is used to delete a single user by providing id.

    Parameter:
    - **user_id** (INT): ID of user to be deleted. **(Required)**

    Return:
    - **None**

    """

    result: UserTable | None = UserService().delete(
        db_session=db_session, entity_id=user_id
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=user_response_message.USER_NOT_FOUND,
        )
