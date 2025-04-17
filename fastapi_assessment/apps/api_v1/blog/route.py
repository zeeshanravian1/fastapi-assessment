"""Blog Route Module.

Description:
- This module is responsible for handling blog routes.

"""

from collections.abc import Sequence
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import ORJSONResponse

from fastapi_assessment.apps.api_v1.blog.service import BlogService
from fastapi_assessment.apps.base.model import BasePaginationData, Message
from fastapi_assessment.core.security import CurrentUser
from fastapi_assessment.database.session import DBSession

from .model import (
    Blog,
    BlogBulkPatch,
    BlogBulkRead,
    BlogBulkUpdate,
    BlogCreate,
    BlogPaginationData,
    BlogPaginationRead,
    BlogPatch,
    BlogRead,
    BlogResponse,
    BlogUpdate,
)

router = APIRouter(prefix="/blog", tags=["Blog"])


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    summary="Create a single blog",
    response_description="Blog created successfully",
)
async def create_blog(
    db_session: DBSession,
    record: BlogCreate,
    current_user: CurrentUser,
    blog_service: BlogService = Depends(lambda: BlogService(model=Blog)),
) -> BlogRead:
    """Create a single blog.

    :Description:
    - This route is used to create a single blog.

    :Args:
    Blog details to be created with following fields:
    - `title` (str): Title of blog. **(Required)**
    - `content` (str): Content of blog. **(Required)**

    :Returns:
    Blog details along with following information:
    - `id` (UUID): Id of blog.
    - `title` (str): Title of blog.
    - `content` (str): Content of blog.
    - `created_at` (datetime): Datetime of blog creation.
    - `updated_at` (datetime): Datetime of blog updation.

    """
    result: Blog = await blog_service.create(
        db_session=db_session, record=record, current_user=current_user
    )

    return BlogRead(
        success=True,
        message="Blog created successfully",
        data=BlogResponse.model_validate(obj=result),
    )


@router.post(
    path="/bulk",
    status_code=status.HTTP_201_CREATED,
    summary="Create multiple blogs",
    response_description="Blogs created successfully",
)
async def create_blogs(
    db_session: DBSession,
    records: list[BlogCreate],
    current_user: CurrentUser,
    blog_service: BlogService = Depends(lambda: BlogService(model=Blog)),
) -> BlogBulkRead:
    """Create multiple blogs.

    :Description:
    - This route is used to create multiple blogs.

    :Args:
    List of blog details to be created with following fields:
    - `title` (str): Title of blog. **(Required)**
    - `content` (str): Content of blog. **(Required)**

    :Returns:
    List of blog details along with following information:
    - `id` (UUID): Id of blog.
    - `title` (str): Title of blog.
    - `content` (str): Content of blog.
    - `created_at` (datetime): Datetime of blog creation.
    - `updated_at` (datetime): Datetime of blog updation.

    """
    results: Sequence[Blog] = await blog_service.create_multiple(
        db_session=db_session,
        records=records,  # type: ignore[arg-type]
        current_user=current_user,
    )

    return BlogBulkRead(
        success=True,
        message="Blogs created successfully",
        data=[BlogResponse.model_validate(obj=result) for result in results],
    )


@router.get(
    path="/bulk",
    status_code=status.HTTP_200_OK,
    summary="Retrieve multiple blogs by IDs",
    response_description="Blogs retrieved successfully",
)
async def read_blogs_by_ids(
    db_session: DBSession,
    blog_ids: Annotated[list[UUID], Query(...)],
    _: CurrentUser,
    blog_service: BlogService = Depends(lambda: BlogService(model=Blog)),
) -> BlogBulkRead:
    """Retrieve multiple blogs by IDs.

    :Description:
    - This route is used to retrieve multiple blogs by their IDs.

    :Args:
    - `blog_ids` (list[UUID]): List of blog IDs. **(Required)**

    :Returns:
    List of blog details along with following information:
    - `id` (UUID): Id of blog.
    - `title` (str): Title of blog.
    - `content` (str): Content of blog.
    - `created_at` (datetime): Datetime of blog creation.
    - `updated_at` (datetime): Datetime of blog updation.

    """
    results: Sequence[Blog] = await blog_service.read_multiple_by_ids(
        db_session=db_session,
        record_ids=blog_ids,  # type: ignore[arg-type]
    )

    return BlogBulkRead(
        success=True,
        message="Blogs retrieved successfully",
        data=[BlogResponse.model_validate(obj=result) for result in results],
    )


@router.get(
    path="/{blog_id}",
    status_code=status.HTTP_200_OK,
    summary="Retrieve a single blog by ID",
    response_description="Blog retrieved successfully",
)
async def read_blog_by_id(
    db_session: DBSession,
    blog_id: Annotated[UUID, "Blog ID"],
    _: CurrentUser,
    blog_service: BlogService = Depends(lambda: BlogService(model=Blog)),
) -> BlogRead:
    """Retrieve a single blog by ID.

    :Description:
    - This route is used to retrieve a single blog by its ID.

    :Args:
    - `blog_id` (UUID): ID of blog. **(Required)**

    :Returns:
    Blog details along with following information:
    - `id` (UUID): Id of blog.
    - `title` (str): Title of blog.
    - `content` (str): Content of blog.
    - `created_at` (datetime): Datetime of blog creation.
    - `updated_at` (datetime): Datetime of blog updation.

    """
    result: Blog | None = await blog_service.read_by_id(
        db_session=db_session, record_id=blog_id
    )

    if not isinstance(result, Blog):
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Blog not found",
                "data": None,
            },
        )

    return BlogRead(
        success=True,
        message="Blog retrieved successfully",
        data=BlogResponse.model_validate(obj=result),
    )


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    summary="Retrieve all blogs",
    response_description="Blogs retrieved successfully",
)
async def read_blogs(
    db_session: DBSession,
    _: CurrentUser,
    order_by: str | None = None,
    desc: bool = False,
    page: int | None = None,
    limit: int | None = None,
    search_by: str | None = None,
    search_query: str | None = None,
    blog_service: BlogService = Depends(lambda: BlogService(model=Blog)),
) -> BlogPaginationRead:
    """Retrieve all blogs.

    :Description:
    - This route is used to retrieve all blogs.

    :Returns:
    List of blog details along with following information:
    - `id` (UUID): Id of blog.
    - `title` (str): Title of blog.
    - `content` (str): Content of blog.
    - `created_at` (datetime): Datetime of blog creation.
    - `updated_at` (datetime): Datetime of blog updation.

    """
    results: BasePaginationData[Blog] = await blog_service.read_all(
        db_session=db_session,
        order_by=order_by,
        desc=desc,
        page=page,
        limit=limit,
        search_by=search_by,
        search_query=search_query,
    )

    return BlogPaginationRead(
        success=True,
        message="Blogs retrieved successfully",
        data=BlogPaginationData.model_validate(obj=results),
    )


@router.put(
    path="/{blog_id}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update a single blog by ID",
    response_description="Blog updated successfully",
)
async def update_blog_by_id(
    db_session: DBSession,
    blog_id: Annotated[UUID, "Blog ID"],
    record: BlogUpdate,
    _: CurrentUser,
    blog_service: BlogService = Depends(lambda: BlogService(model=Blog)),
) -> BlogRead:
    """Update a single blog by ID.

    :Description:
    - This route is used to update a single blog by its ID.

    :Args:
    - `blog_id` (UUID): ID of blog. **(Required)**
    Blog details to be updated with following fields:
    - `title` (str): Title of blog. **(Required)**
    - `content` (str): Content of blog. **(Required)**

    :Returns:
    Blog details along with following information:
    - `id` (UUID): Id of blog.
    - `title` (str): Title of blog.
    - `content` (str): Content of blog.
    - `created_at` (datetime): Datetime of blog creation.
    - `updated_at` (datetime): Datetime of blog updation.

    """
    result: Blog | None = await blog_service.update_by_id(
        db_session=db_session, record_id=blog_id, record=record
    )

    if not isinstance(result, Blog):
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Blog not found",
                "data": None,
            },
        )

    return BlogRead(
        success=True,
        message="Blog updated successfully",
        data=BlogResponse.model_validate(obj=result),
    )


@router.put(
    path="/bulk",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update multiple blogs by IDs",
    response_description="Blogs updated successfully",
)
async def update_blogs_by_ids(
    db_session: DBSession,
    records: list[BlogBulkUpdate],
    _: CurrentUser,
    blog_service: BlogService = Depends(lambda: BlogService(model=Blog)),
) -> BlogBulkRead:
    """Update multiple blogs by IDs.

    :Description:
    - This route is used to update multiple blogs by their IDs.

    :Args:
    List of blog details to be updated with following fields:
    - `id` (UUID): Id of blog. **(Required)**
    - `title` (str): Title of blog. **(Required)**
    - `content` (str): Content of blog. **(Required)**

    :Returns:
    List of blog details along with following information:
    - `id` (UUID): Id of blog.
    - `title` (str): Title of blog.
    - `content` (str): Content of blog.
    - `created_at` (datetime): Datetime of blog creation.
    - `updated_at` (datetime): Datetime of blog updation.

    """
    results: Sequence[Blog] = await blog_service.update_multiple_by_ids(
        db_session=db_session,
        records=records,  # type: ignore[arg-type]
    )

    return BlogBulkRead(
        success=True,
        message="Blogs updated successfully",
        data=[BlogResponse.model_validate(obj=result) for result in results],
    )


@router.patch(
    path="/{blog_id}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Patch a single blog by ID",
    response_description="Blog patched successfully",
)
async def patch_blog_by_id(
    db_session: DBSession,
    blog_id: Annotated[UUID, "Blog ID"],
    record: BlogPatch,
    _: CurrentUser,
    blog_service: BlogService = Depends(lambda: BlogService(model=Blog)),
) -> BlogRead:
    """Patch a single blog by ID.

    :Description:
    - This route is used to patch a single blog by its ID.

    :Args:
    - `blog_id` (UUID): ID of blog. **(Required)**
    Blog details to be patched with following fields:
    - `title` (str): Title of blog. **(Optional)**
    - `content` (str): Content of blog. **(Optional)**

    :Returns:
    Blog details along with following information:
    - `id` (UUID): Id of blog.
    - `title` (str): Title of blog.
    - `content` (str): Content of blog.
    - `created_at` (datetime): Datetime of blog creation.
    - `updated_at` (datetime): Datetime of blog updation.

    """
    result: Blog | None = await blog_service.update_by_id(
        db_session=db_session, record_id=blog_id, record=record
    )

    if not isinstance(result, Blog):
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Blog not found",
                "data": None,
            },
        )

    return BlogRead(
        success=True,
        message="Blog patched successfully",
        data=BlogResponse.model_validate(obj=result),
    )


@router.patch(
    path="/bulk",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Patch multiple blogs by IDs",
    response_description="Blogs patched successfully",
)
async def patch_blogs_by_ids(
    db_session: DBSession,
    records: list[BlogBulkPatch],
    _: CurrentUser,
    blog_service: BlogService = Depends(lambda: BlogService(model=Blog)),
) -> BlogBulkRead:
    """Patch multiple blogs by IDs.

    :Description:
    - This route is used to patch multiple blogs by their IDs.

    :Args:
    List of blog details to be patched with following fields:
    - `id` (UUID): Id of blog. **(Required)**
    - `title` (str): Title of blog. **(Optional)**
    - `content` (str): Content of blog. **(Optional)**

    :Returns:
    List of blog details along with following information:
    - `id` (UUID): Id of blog.
    - `title` (str): Title of blog.
    - `content` (str): Content of blog.
    - `created_at` (datetime): Datetime of blog creation.
    - `updated_at` (datetime): Datetime of blog updation.

    """
    results: Sequence[Blog] = await blog_service.update_multiple_by_ids(
        db_session=db_session,
        records=records,  # type: ignore[arg-type]
    )

    return BlogBulkRead(
        success=True,
        message="Blogs patched successfully",
        data=[BlogResponse.model_validate(obj=result) for result in results],
    )


@router.delete(
    path="/{blog_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a single blog by ID",
    response_description="Blog deleted successfully",
)
async def delete_blog_by_id(
    db_session: DBSession,
    blog_id: Annotated[UUID, "Blog ID"],
    _: CurrentUser,
    blog_service: BlogService = Depends(lambda: BlogService(model=Blog)),
) -> None:
    """Delete a single blog by ID.

    :Description:
    - This route is used to delete a single blog by its ID.

    :Args:
    - `blog_id` (UUID): ID of blog. **(Required)**

    :Returns:
    - `None`: No content.

    """
    result: Message | None = await blog_service.delete_by_id(
        db_session=db_session, record_id=blog_id
    )

    if not isinstance(result, Message):
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Blog not found",
                "data": None,
            },
        )


@router.delete(
    path="/bulk",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete multiple blogs by IDs",
    response_description="Blogs deleted successfully",
)
async def delete_blogs_by_ids(
    db_session: DBSession,
    blog_ids: Annotated[list[UUID], Query(...)],
    _: CurrentUser,
    blog_service: BlogService = Depends(lambda: BlogService(model=Blog)),
) -> None:
    """Delete multiple blogs by IDs.

    :Description:
    - This route is used to delete multiple blogs by their IDs.

    :Args:
    - `blog_ids` (list[UUID]): List of blog IDs. **(Required)**

    :Returns:
    - `None`: No content.

    """
    result: Message | None = await blog_service.delete_multiple_by_ids(
        db_session=db_session,
        record_ids=blog_ids,  # type: ignore[arg-type]
    )

    if not isinstance(result, Message):
        return ORJSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Blogs not found",
                "data": None,
            },
        )
