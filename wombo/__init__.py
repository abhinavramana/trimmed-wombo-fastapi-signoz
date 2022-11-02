import logging
import os
import nest_asyncio
from opentelemetry.instrumentation.logging import LoggingInstrumentor

LoggingInstrumentor().instrument(set_logging_format=True)

# Disabling basicConfig to allow OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
if os.getenv("OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED", "false").lower() == "false":
    logging.basicConfig(level=logging.INFO, force=True)  # Should happen before any logging
logging.info("Initialized the logger...")

nest_asyncio.apply()
