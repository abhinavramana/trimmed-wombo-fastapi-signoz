import json
import logging
import time
from typing import Any, Dict
from fastapi import Request
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import ClientDisconnect
from starlette.responses import JSONResponse


logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

def bytes_to_dict(bytes_object: bytes) -> Dict[str, Any]:
    if bytes_object is None:
        return {}
    return json.loads(bytes_object.decode('utf-8'))


def get_stats_json(start_time: float, request: Request, response_status_code: int) -> Dict[str, Any]:
    run_time = time.time() - start_time
    # Since user id is generated during auth, it may not be present if (i) auth fails or (ii)
    # a route not requiring auth is being used
    try:
        user_id = request.state.__getattr__("user_id")
    except AttributeError:
        user_id = None
    # Place the necessary stats into the logs as a JSON object, avoid the base route on the app
    stats_json = {
        "user_id": user_id,
        "path": f"{request.method}-{request.url.path}",
        "response_status_code": response_status_code,
        "run_time": run_time,
        "headers": request.headers.items(),  # Starlette Header is not serializable
    }
    return stats_json


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Record the actual processing time for the request
        start_time = time.time()
        try:
            response = await call_next(request)
            response_status_code = response.status_code
            stats_json = get_stats_json(start_time, request, response_status_code)
        except ClientDisconnect:
            # We don't want to handle this and logs get cluttered
            stats_json = get_stats_json(start_time, request, status.HTTP_418_IM_A_TEAPOT)
            stats_json["error_reason"] = "ClientDisconnect"
            logger.info(stats_json)
            response = JSONResponse(stats_json, status.HTTP_418_IM_A_TEAPOT)
        except Exception as ex:
            # Since this was unexpected exception
            stats_json = get_stats_json(start_time, request, status.HTTP_500_INTERNAL_SERVER_ERROR)
            json_response_body = {"detail": repr(ex)}
            response = JSONResponse(json_response_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
            logger.error(json_response_body, exc_info=True)

        logger.info(stats_json)
        return response
