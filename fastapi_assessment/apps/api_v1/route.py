"""API V1 Route module.

Description:
- This module is used to create v1 routes for application.

"""

from fastapi import APIRouter

from .blog.route import router as blog_router
from .user.route import router as user_router

router = APIRouter(prefix="/v1")


# Include all file routes
router.include_router(router=blog_router)
router.include_router(router=user_router)
