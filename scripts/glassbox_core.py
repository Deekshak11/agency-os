
"""
Universal Glass Box Telemetry Core
"""
import modal
import os
import json
from datetime import datetime

# Shared Volume for all agents
log_vol = modal.Volume.from_name("agency-os-logs", create_if_missing=True)

def log_event(event_type: str, entity_id: str, data: dict = None, agent_name: str = "unknown"):
    """
    Emits a structured event to the Glass Box.
    
    Args:
        event_type (str): START, SUCCESS, ERROR, RETRY, PROGRESS, etc.
        entity_id (str): Unique identifier for the item being processed (e.g., email, lead_id).
        data (dict): Contextual metadata (reason, url, duration).
        agent_name (str): Name of the script/agent reporting the event.
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "agent": agent_name,
        "event": event_type,
        "entity": entity_id,
        "data": data or {}
    }
    
    safe_agent = "".join(x for x in agent_name if x.isalnum() or x in "-_")
    safe_entity = "".join(x for x in entity_id if x.isalnum() or x in "-_.@")

    # Determine log path (Remote vs Local)
    base_dir = "/root/logs/glassbox" if os.path.exists("/root/logs") else "logs/glassbox"
    log_path = os.path.join(base_dir, safe_agent, f"{safe_entity}.jsonl")
    
    try:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"[GlassBox Error] Failed to log {event_type} for {entity_id}: {e}")

