"""
Routes Module

Description:
- This module is used to create routes.

"""

from fastapi import APIRouter

from .role import router as role_router
from .user import router as user_router

router = APIRouter()


# Include all file routes
router.include_router(role_router)
router.include_router(user_router)
