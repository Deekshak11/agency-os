
import modal
import os
import sys
import time
import json
from datetime import datetime

log_vol = modal.Volume.from_name("agency-os-logs")
app = modal.App("glass-box-monitor")

@app.function(volumes={"/root/logs": log_vol})
def get_log_stats__cli():
    import os
    import json
    
    stats = {
        "total_leads": 0,
        "processed": 0,
        "success": 0,
        "errors": 0,
        "retries": 0,
        "active": 0,
        "last_events": []
    }
    
    log_dir = "/root/logs/glassbox"
    if not os.path.exists(log_dir):
        return stats
        
    for root, dirs, files in os.walk(log_root):
        for file in files:
            if not file.endswith(".jsonl"):
                continue
            
            stats["total_leads"] += 1
            path = os.path.join(root, file)
            
            try:
                with open(path, "r") as f:
                    lines = f.readlines()
                    if not lines: continue
                    
                    last_line = json.loads(lines[-1])
                    evt = last_line.get("event")
                    
                    if evt == "SUCCESS":
                        stats["success"] += 1
                    elif evt in ["ERROR", "FATAL", "EXHAUSTED"]:
                        stats["errors"] += 1
                    elif evt in ["START", "PROGRESS"]:
                        stats["active"] += 1
                    elif evt == "RETRY":
                        stats["retries"] += 1
                        
                    stats["last_events"].append({
                        "lead": last_line.get("entity", file.replace(".jsonl", "")),
                        "event": evt,
                        "time": last_line.get("timestamp", "")
                    })
            except:
                continue

    stats["last_events"].sort(key=lambda x: x["time"], reverse=True)
    stats["last_events"] = stats["last_events"][:10]
    return stats

@app.local_entrypoint()
def main():
    print("🖥️  AGENCY OS // SYSTEMS MONITOR")
    print("--------------------------------")
    try:
        while True:
            stats = get_log_stats__cli.remote()
            print("\n" * 2)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚀 Active: {stats['active']} | ✅ Done: {stats['success']} | ❌ Err: {stats['errors']}")
            print("Latest:")
            for e in stats['last_events']:
                print(f" > {e['time'][11:19]} [{e['event']}] {e['lead']}")
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nExiting.")
