"""
Role Constants Module

Description:
- This module is used to define role constants.

"""

from datetime import datetime, timezone

ID: int = 1
CREATED_AT: datetime = datetime.now(tz=timezone.utc)
UPDATED_AT: datetime = datetime.now(tz=timezone.utc)
