# Normal third party imports
import logging
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from wombo.logging_middleware import LoggingMiddleware

logger = logging.getLogger(__name__)
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

app = FastAPI(**opts)
app.add_middleware(LoggingMiddleware)
app.state.health_checks_since_neptune_check = 0


# Manage the CORS Middleware being added to the app
origins = []
regex_origins = ""

origins.append("https://www.wombo.net")
origins.append("http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=regex_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health_check():
    x = datetime.now()
    logger.warn(f"Random logs : {x}")
    return dict(now=x)
