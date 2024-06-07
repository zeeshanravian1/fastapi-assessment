"""
Core Response Message Module

Description:
- This module is responsible for core response messages.

"""

from ..constants.base import MAX_CONTENT_LENGTH


class CoreResponseMessage:
    """
    Core Response Message Class

    Description:
    - This class is used to define core response messages.

    """

    INVALID_TOKEN: str = "Invalid token"
    TOKEN_EXPIRED: str = "Token expired"
    INTEGRITY_ERROR: str = "Integrity error"
    INVALID_RESPONSE_BODY: str = "Invalid response body"
    INTERNAL_SERVER_ERROR: str = "Internal server error"
    PAYLOAD_TOO_LARGE: str = (
        "Payload too large."
        + f"Maximum content length is {MAX_CONTENT_LENGTH} bytes"
    )


core_response_message = CoreResponseMessage()
