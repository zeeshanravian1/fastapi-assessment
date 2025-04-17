"""Middlewares Module.

Description:
- This module contains all middlewares used in project.

"""

import logging
import re
from typing import Any

from fastapi import Request, Response, status
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import ORJSONResponse
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from sqlalchemy.exc import IntegrityError

from .response_message import core_response_message

exception_logger: logging.Logger = logging.getLogger(__name__)


async def exception_handling(
    request: Request, call_next: Any
) -> ORJSONResponse | Response:
    """Exception Handling Middleware.

    :Description:
    - This function is used to handle exceptions.

    :Args:
    - `request` (Request): Request object. **(Required)**
    - `call_next` (Callable): Next function to be called. **(Required)**

    :Returns:
    - **response** (Response): Response object.

    """
    try:
        response: Response = await call_next(request)

    except ExpiredSignatureError:
        return ORJSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "message": core_response_message.TOKEN_EXPIRED,
                "data": None,
                "error": core_response_message.TOKEN_EXPIRED,
            },
        )

    except InvalidSignatureError:
        return ORJSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "message": core_response_message.INVALID_TOKEN,
                "data": None,
                "error": core_response_message.INVALID_TOKEN,
            },
        )

    except IntegrityError as err:
        err_message: str = (
            str(err.orig)
            .split("DETAIL:", maxsplit=1)[0]
            .replace("Key", "")
            .replace("(", "")
            .replace(")", "")
            .strip()
        )
        err_message = re.sub(
            pattern=r"in table.*", repl="", string=err_message
        ).strip()

        return ORJSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "success": False,
                "message": "Integrity Error",
                "data": None,
                "error": err_message,
            },
        )

    except ResponseValidationError as err:
        exception_logger.exception(msg=err)
        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "message": core_response_message.INVALID_RESPONSE_BODY,
                "data": None,
                "error": core_response_message.INVALID_RESPONSE_BODY,
            },
        )

    except Exception as err:
        exception_logger.exception(msg=err)
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": core_response_message.INTERNAL_SERVER_ERROR,
                "data": None,
                "error": str(err),
            },
        )
    return response
