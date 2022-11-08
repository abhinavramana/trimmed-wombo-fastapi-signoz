from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.environment_variables import OTEL_EXPORTER_OTLP_ENDPOINT

reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT))
metrics.set_meter_provider(MeterProvider(metric_readers=[reader]))
meter = metrics.get_meter("worker_vqgan", "0.1.0")

requests_counter = meter.create_counter(
    name="requests",
    description="number of requests"
)

health_checks_counter = meter.create_counter(
    name="health_checks",
    description="number of requests"
)