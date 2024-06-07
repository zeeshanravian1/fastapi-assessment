"""
Authentication Route Module

Description:
- This module is responsible for handling auth routes.
- It is used to login, refresh token, logout user.

"""

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from ..database.session import get_session
from ..schemas.auth import LoginReadSchema, RegisterReadSchema, RegisterSchema
from ..services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


# Register route
@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register User",
    response_description="User registered successfully",
)
async def register(
    record: RegisterSchema,
    db_session: Session = Depends(get_session),
) -> RegisterReadSchema:
    """
    Register.

    Description:
    - This route is used to register user.

    Parameter:
    - **email** (STR): Email of user. **(Required)**
    - **username** (STR): Username of user. **(Required)**
    - **password** (STR): Password of user. **(Required)**

    Return:
    - **token_type** (STR): Token type of user.
    - **access_token** (STR): Access token of user.
    - **refresh_token** (STR): Refresh token of user.
    - **id** (INT): Id of user.
    - **name** (STR): Name of user.
    - **username** (STR): Username of user.
    - **email** (STR): Email of user.
    - **role_id** (INT): Id of role.
    - **created_at** (DATETIME): Datetime of user creation.
    - **updated_at** (DATETIME): Datetime of user updation.

    """

    return AuthService().register(db_session, record)


# Login route
@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    summary="Perform Authentication",
    response_description="User logged in successfully",
)
async def login(
    db_session: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> LoginReadSchema:
    """
    Login.

    Description:
    - This route is used to login user.

    Parameter:
    - **email or username** (STR): Email or username of user. **(Required)**
    - **password** (STR): Password of user. **(Required)**

    Return:
    - **token_type** (STR): Token type of user.
    - **access_token** (STR): Access token of user.
    - **refresh_token** (STR): Refresh token of user.
    - **id** (INT): Id of user.
    - **name** (STR): Name of user.
    - **username** (STR): Username of user.
    - **email** (STR): Email of user.
    - **role_id** (INT): Id of role.
    - **created_at** (DATETIME): Datetime of user creation.
    - **updated_at** (DATETIME): Datetime of user updation.

    """

    user: LoginReadSchema | dict[str, str] = AuthService().login(
        db_session, form_data
    )

    if isinstance(user, dict):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=user["detail"],
        )

    return user
