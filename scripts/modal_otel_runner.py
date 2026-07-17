"""
Modal Runner with OTEL Tracing
V1.0.0 | LangSmith-Compatible Observability

Usage:
    modal run scripts/modal_otel_runner.py --workflow lead-gen --entity-id abc123
"""
import modal
import os
import sys
import json
from datetime import datetime
from typing import Optional, Dict, Any

# Add scripts to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = modal.App("agency-os-otel-runner")

log_vol = modal.Volume.from_name("agency-os-logs")
auth_vol = modal.Volume.from_name("agency-os-auth")

@app.function(
    volumes={"/root/logs": log_vol, "/root/auth": auth_vol},
    timeout=600,
    retries=2
)
def run_with_tracing(
    workflow: str,
    entity_id: str,
    config: Optional[Dict[str, Any]] = None
):
    from otel_tracing import trace_workflow, trace_tool_execution, trace_llm_call, TracedRunner
    
    runner = TracedRunner(f"{workflow}-{entity_id}")
    runner.start({"workflow": workflow, "entity_id": entity_id})
    
    try:
        # Trace workflow start
        trace_workflow(workflow, entity_id, "START")
        runner.log("init", {"timestamp": datetime.now().isoformat()})
        
        # === WORKFLOW STEPS ===
        # Replace with your actual workflow logic
        # Example:
        # 
        # 1. Fetch data
        # runner.log("fetch_data")
        # with trace_span("fetch_lead_data", {"entity_id": entity_id}):
        #     lead_data = fetch_lead(entity_id)
        # 
        # 2. Enrich
        # runner.log("enrich")
        # trace_tool_execution("enricher", 150.0, success=True)
        # 
        # 3. Generate content
        # runner.log("generate")
        # trace_llm_call("MiniMax-2.5", 500, 200, 2500.0, success=True)
        # 
        # 4. Export
        # runner.log("export")
        # trace_tool_execution("exporter", 80.0, success=True)
        
        runner.log("complete")
        trace_workflow(workflow, entity_id, "SUCCESS")
        runner.complete(success=True, summary={"entity_id": entity_id})
        
        return {"status": "success", "entity_id": entity_id}
        
    except Exception as e:
        error_msg = str(e)
        runner.log("error", {"error": error_msg})
        trace_workflow(workflow, entity_id, "ERROR", {"error": error_msg})
        runner.complete(success=False, summary={"error": error_msg})
        
        # Log to glassbox
        log_path = f"/root/logs/glassbox/{workflow}/{entity_id}.jsonl"
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "a") as f:
            f.write(json.dumps({
                "timestamp": datetime.now().isoformat(),
                "workflow": workflow,
                "entity_id": entity_id,
                "event": "ERROR",
                "error": error_msg
            }) + "\n")
        
        raise

@app.local_entrypoint()
def main(workflow: str = "test", entity_id: str = "local-test"):
    print(f"Starting {workflow} for {entity_id}")
    result = run_with_tracing.remote(workflow, entity_id)
    print(f"Result: {result}")
