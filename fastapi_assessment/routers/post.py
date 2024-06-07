"""
Role Route Module

Description:
- This module is responsible for handling role routes.
- It is used to create, get, update, delete role details.

"""

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from ..database.session import get_session
from ..models.post import PostTable
from ..response_messages.post import post_response_message
from ..schemas.post import PostCreateSchema, PostReadSchema, PostUpdateSchema
from ..services.post import PostService

router = APIRouter(prefix="/post", tags=["Post"])


# Create a single post route
@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    summary="Create a single post",
    response_description="Post created successfully",
)
async def create_post(
    record: PostCreateSchema,
    db_session: Session = Depends(get_session),
) -> PostReadSchema:
    """
    Create a single post

    Description:
    - This route is used to create a single post.

    Parameter:
    Post details to be created with following fields:
    - **text** (STR): Text of post. **(Required)**

    Return:
    Post details along with following information:
    - **id** (INT): Id of post.
    - **text** (STR): Text of post.
    - **created_at** (DATETIME): Datetime of post creation.
    - **updated_at** (DATETIME): Datetime of post updation.

    """

    result: PostTable = PostService().create(
        db_session=db_session, entity=record
    )

    return PostReadSchema.model_validate(obj=result)


# Get a single post by id route
@router.get(
    path="/{post_id}",
    status_code=status.HTTP_200_OK,
    summary="Get a single post by providing id",
    response_description="Post details fetched successfully",
)
async def get_post_by_id(
    post_id: int,
    db_session: Session = Depends(get_session),
) -> PostReadSchema:
    """
    Get a single post

    Description:
    - This route is used to get a single post by providing id.

    Parameter:
    - **post_id** (INT): ID of post to be fetched. **(Required)**

    Return:
    Get a single post with following information:
    - **id** (INT): Id of post.
    - **text** (STR): Text of post.
    - **created_at** (DATETIME): Datetime of post creation.
    - **updated_at** (DATETIME): Datetime of post updation.

    """

    result: PostTable | None = PostService().read_by_id(
        db_session=db_session, entity_id=post_id
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=post_response_message.POST_NOT_FOUND,
        )

    return PostReadSchema.model_validate(obj=result)


# Get all posts route
@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    summary="Get all posts",
    response_description="All posts fetched successfully",
)
async def get_all_posts(
    db_session: Session = Depends(get_session),
):
    """
    Get all posts

    Description:
    - This route is used to get all posts.

    Return:
    Get all posts with following information:
    - **id** (INT): Id of post.
    - **text** (STR): Text of post.
    - **created_at** (DATETIME): Datetime of post creation.
    - **updated_at** (DATETIME): Datetime of post updation.

    """

    result: list[PostTable] = PostService().read_all(db_session=db_session)

    return result


# Update a single post route
@router.put(
    path="/{post_id}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update a single post by providing id",
    response_description="Post updated successfully",
)
async def update_post(
    post_id: int,
    record: PostUpdateSchema,
    db_session: Session = Depends(get_session),
) -> PostReadSchema:
    """
    Update a single post

    Description:
    - This route is used to update a single post by providing id.

    Parameter:
    - **post_id** (INT): ID of post to be updated. **(Required)**
    Post details to be updated with following fields:
    - **text** (STR): Text of post. **(Required)**

    Return:
    Post details along with following information:
    - **id** (INT): Id of post.
    - **text** (STR): Text of post.
    - **created_at** (DATETIME): Datetime of post creation.
    - **updated_at** (DATETIME): Datetime of post updation.

    """

    result: PostTable | None = PostService().update(
        db_session=db_session, entity_id=post_id, entity=record
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=post_response_message.POST_NOT_FOUND,
        )

    return PostReadSchema.model_validate(obj=result)


# Delete a single post route
@router.delete(
    path="/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a single post by providing id",
    response_description="Post deleted successfully",
)
async def delete_post(
    post_id: int,
    db_session: Session = Depends(get_session),
) -> None:
    """
    Delete a single post

    Description:
    - This route is used to delete a single post by providing id.

    Parameter:
    - **post_id** (INT): ID of post to be deleted. **(Required)**

    Return:
    - **None**

    """

    result: PostTable | None = PostService().delete(
        db_session=db_session, entity_id=post_id
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=post_response_message.POST_NOT_FOUND,
        )
