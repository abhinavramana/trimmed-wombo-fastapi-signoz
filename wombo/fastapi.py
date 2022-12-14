# Normal third party imports
import logging
from datetime import datetime

from fastapi import FastAPI
from fastapi import HTTPException, status
from starlette.middleware import Middleware

from wombo.db_table import create_clean_table_if_needed
from wombo.logger_stuff import get_logger
from wombo.middleware import LoggingMiddleware, WomboCORSMiddleware




logger = get_logger(__name__)
# Decide if the current environment is production or testing
opts = {
    "docs_url": "/signoz",
    "redoc_url": None
}
"""
# Should happen even before app starts
if ENABLE_OPENTELEMETRY:
    os.environ["OTEL_EXPORTER_OTLP_TRACES_ENDPOINT"] = f"{OTEL_EXPORTER_OTLP_ENDPOINT}/v1/traces"
    configure_opentelemetry(
        service_name=OTEL_SERVICE_NAME,
        # TODO : Somehow get the paint-task version and populate here to compare canary/staging versions
        service_version="1.0.0",
        span_exporter_endpoint=OTEL_EXPORTER_OTLP_ENDPOINT,
        span_exporter_insecure=True  # Allow everything within AWS
        # Add log_level=debug here
    )
"""

create_clean_table_if_needed()

app = FastAPI(**opts)
app.state.health_checks_since_neptune_check = 0

"""
https://github.com/SigNoz/signoz/issues/1692: The add_middleware adds the middleware at the beginning (or top) of list,
leading to a situation where logging middleware gets processed before the OpenTelemetry middleware. Since the trace is
not started yet, you see the empty context. I added this workaround to push the logging middleware to the bottom, so
it gets processed later when there is trace context
"""

app.user_middleware.append(Middleware(LoggingMiddleware))
app.user_middleware.append(Middleware(WomboCORSMiddleware))
app.middleware_stack = app.build_middleware_stack()
logger.info("Initialized Middlewares...")


@app.get("/log")
async def health_check():
    x = datetime.now()
    logger.warn(f"Random logs : {x}")
    return dict(now=x)


@app.get("/exception_dont_works")
async def exception_dont_works():
    try:
        raise ValueError("sadness")
    except Exception as ex:
        logger.error(ex, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Got sadness")


@app.get("/exception_works")
async def exception_works():
    raise ValueError("sadness")
