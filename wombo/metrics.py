from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from os import getenv
OTEL_SERVICE_NAME = getenv('OTEL_SERVICE_NAME', 'trimmed-fastapi')
OTEL_EXPORTER_OTLP_ENDPOINT = getenv('OTEL_EXPORTER_OTLP_ENDPOINT', 'http://localhost:4317')

resource = Resource(attributes={
    SERVICE_NAME: OTEL_SERVICE_NAME
})
reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT))
metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=[reader]))
meter = metrics.get_meter("worker_vqgan")

requests_counter = meter.create_counter(
    name="requests",
    description="number of requests"
)

health_checks_counter = meter.create_counter(
    name="health_checks",
    description="number of requests"
)