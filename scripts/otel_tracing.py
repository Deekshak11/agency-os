"""
OTEL Tracing Core - LangSmith-Compatible Observability
V1.0.0 | OpenTelemetry + LangSmith Integration
"""
import os
import time
import json
from typing import Optional, Dict, Any, List
from contextlib import contextmanager
from datetime import datetime

try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.resources import Resource, SERVICE_NAME
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False
    trace = None

AGENT_NAME = "agency-os"

class AgencyTracer:
    def __init__(self, service_name: str = "agency-os"):
        self.service_name = service_name
        self.tracer = None
        self._initialized = False
        
    def initialize(self):
        if self._initialized:
            return
            
        if not OTEL_AVAILABLE:
            print("[OTEL] opentelemetry not installed. Run: pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp")
            return
            
        langsmith_key = os.getenv("LANGSMITH_API_KEY")
        otel_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "https://api.langsmith.com/v1/traces")
        otel_headers = os.getenv("OTEL_EXPORTER_OTLP_HEADERS", "")
        
        if langsmith_key and "langsmith" in otel_endpoint:
            if otel_headers:
                otel_headers += f",x-api-key={langsmith_key}"
            else:
                otel_headers = f"x-api-key={langsmith_key}"
            os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = otel_headers
            
        resource = Resource.create({
            SERVICE_NAME: self.service_name,
            "agency.version": "1.0.0",
            "agency.environment": os.getenv("AGENCY_ENV", "production")
        })
        
        provider = TracerProvider(resource=resource)
        
        try:
            exporter = OTLPSpanExporter(
                endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "https://api.langsmith.com/v1/traces"),
                insecure=not otel_endpoint.startswith("https")
            )
            provider.add_span_processor(BatchSpanProcessor(exporter))
        except Exception as e:
            print(f"[OTEL] Failed to initialize exporter: {e}")
            
        trace.set_tracer_provider(provider)
        self.tracer = trace.get_tracer(self.service_name)
        self._initialized = True
        print(f"[OTEL] Initialized for {self.service_name}")

_tracer_instance: Optional[AgencyTracer] = None

def get_tracer(service_name: str = "agency-os") -> AgencyTracer:
    global _tracer_instance
    if _tracer_instance is None:
        _tracer_instance = AgencyTracer(service_name)
        _tracer_instance.initialize()
    return _tracer_instance

@contextmanager
def trace_span(
    name: str,
    attributes: Optional[Dict[str, Any]] = None,
    parent: Any = None
):
    tracer = get_tracer()
    
    if not tracer._initialized or tracer.tracer is None:
        yield None
        return
        
    with tracer.tracer.start_as_current_span(name) as span:
        if attributes:
            for k, v in attributes.items():
                if isinstance(v, (str, int, float, bool)):
                    span.set_attribute(k, v)
                else:
                    span.set_attribute(k, str(v))
        yield span

def trace_llm_call(
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
    latency_ms: float,
    success: bool = True,
    error: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
):
    with trace_span("llm.call", {
        "llm.model": model,
        "llm.prompt_tokens": prompt_tokens,
        "llm.completion_tokens": completion_tokens,
        "llm.total_tokens": prompt_tokens + completion_tokens,
        "llm.latency_ms": latency_ms,
        "llm.success": success,
        "llm.error": error or ""
    }):
        pass

def trace_tool_execution(
    tool_name: str,
    duration_ms: float,
    success: bool = True,
    error: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
):
    attrs = {
        "tool.name": tool_name,
        "tool.duration_ms": duration_ms,
        "tool.success": success,
        "tool.error": error or ""
    }
    if metadata:
        attrs.update({f"tool.{k}": v for k, v in metadata.items()})
    
    with trace_span("tool.execution", attrs):
        pass

def trace_agent_loop(
    agent_name: str,
    mode: str,
    iteration: int,
    decision: str,
    metadata: Optional[Dict[str, Any]] = None
):
    attrs = {
        "agent.name": agent_name,
        "agent.mode": mode,
        "agent.iteration": iteration,
        "agent.decision": decision
    }
    if metadata:
        attrs.update({f"agent.{k}": v for k, v in metadata.items()})
    
    with trace_span("agent.loop", attrs):
        pass

def trace_workflow(
    workflow_name: str,
    entity_id: str,
    event: str,
    metadata: Optional[Dict[str, Any]] = None
):
    attrs = {
        "workflow.name": workflow_name,
        "workflow.entity_id": entity_id,
        "workflow.event": event
    }
    if metadata:
        attrs.update({f"workflow.{k}": v for k, v in metadata.items()})
    
    with trace_span("workflow.event", attrs):
        pass

class TracedRunner:
    def __init__(self, runner_name: str):
        self.runner_name = runner_name
        self.start_time = None
        
    def start(self, metadata: Optional[Dict[str, Any]] = None):
        self.start_time = time.time()
        attrs = {"runner.name": self.runner_name}
        if metadata:
            attrs.update(metadata)
        get_tracer()._current_span = trace_span("runner.start", attrs)
        print(f"[{self.runner_name}] Started at {datetime.now().isoformat()}")
        
    def log(self, step: str, metadata: Optional[Dict[str, Any]] = None):
        attrs = {"runner.step": step, "runner.elapsed_ms": (time.time() - self.start_time) * 1000}
        if metadata:
            attrs.update(metadata)
        with trace_span(f"runner.{step}", attrs):
            print(f"[{self.runner_name}] {step}")
            
    def complete(self, success: bool = True, summary: Optional[Dict[str, Any]] = None):
        duration_ms = (time.time() - self.start_time) * 1000
        attrs = {
            "runner.duration_ms": duration_ms,
            "runner.success": success
        }
        if summary:
            attrs.update({f"runner.summary.{k}": v for k, v in summary.items()})
        with trace_span("runner.complete", attrs):
            print(f"[{self.runner_name}] Completed in {duration_ms:.0f}ms (success={success})")
        self.start_time = None
