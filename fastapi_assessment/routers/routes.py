"""
Routes Module

Description:
- This module is used to create routes.

"""

from fastapi import APIRouter

from .role import router as role_router

router = APIRouter()


# Include all file routes
router.include_router(role_router)
