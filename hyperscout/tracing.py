import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry.sdk.resources import Resource

def setup_tracing():
    """
    Configures OpenTelemetry tracing to output to the console.
    """
    resource = Resource.create({"service.name": "hyperscout"})

    # Create a TracerProvider
    provider = TracerProvider(resource=resource)

    # Create a ConsoleSpanExporter
    exporter = ConsoleSpanExporter()

    # Create a SimpleSpanProcessor and add the exporter
    processor = SimpleSpanProcessor(exporter)

    # Add the processor to the provider
    provider.add_span_processor(processor)

    # Set the provider
    trace.set_tracer_provider(provider)

def get_tracer(name):
    """
    Returns a tracer instance.
    """
    return trace.get_tracer(name)
