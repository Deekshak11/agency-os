#!/usr/bin/env python3
import json, sys

config = {
  "agents": {"defaults": {"model": {"primary": "inference/glm-5.1"}}},
  "models": {"mode": "merge", "providers": {"inference": {"baseUrl": "https://inference.local/v1", "apiKey": "unused", "api": "openai-completions", "models": [{"compat": {"supportsStore": False}, "id": "glm-5.1", "name": "inference/glm-5.1", "reasoning": False, "input": ["text"], "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0}, "contextWindow": 131072, "maxTokens": 4096}]}}},
  "channels": {"defaults": {}, "telegram": {"accounts": {"default": {"botToken": "openshell:resolve:env:TELEGRAM_BOT_TOKEN", "enabled": True, "groupPolicy": "open", "dmPolicy": "allowlist", "allowFrom": ["1916285808"]}}, "enabled": True}},
  "gateway": {"mode": "local", "controlUi": {"allowInsecureAuth": True, "dangerouslyDisableDeviceAuth": True, "allowedOrigins": ["http://127.0.0.1:18789", "https://leather-provincial-listing-installations.trycloudflare.com"]}, "trustedProxies": ["127.0.0.1", "::1"], "auth": {"token": "e4b32332607a6d4e4e81ac7118ca08b1ab652970bd66f0cfcd732a0c8c19d028"}},
  "wizard": {"lastRunAt": "2026-04-15T14:04:34.088Z", "lastRunVersion": "2026.4.2", "lastRunCommand": "doctor", "lastRunMode": "local"},
  "meta": {"lastTouchedVersion": "2026.4.2", "lastTouchedAt": "2026-04-15T14:04:34.213Z"}
}

json_str = json.dumps(config, indent=2)

# Write to VPS temp file
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('[REDACTED_IP]', username='root', password='Azaxacavab@11', timeout=15)

# Write file to VPS
sftp = ssh.open_sftp()
with sftp.open('/tmp/fix_config.py', 'w') as f:
    f.write('import json\n')
    f.write('cfg=' + repr(config) + '\n')
    f.write('with open("/sandbox/.openclaw/openclaw.json","w") as f: json.dump(cfg, f, indent=2)\n')
    f.write('print("written")\n')
sftp.close()

# Execute inside sandbox pod via openshell exec
stdin, stdout, stderr = ssh.exec_command('openshell sandbox exec my-assistant -- python3 /tmp/fix_config.py 2>&1', timeout=15)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print(out)
if err.strip(): print('ERR:', err)

# Verify
stdin2, stdout2, stderr2 = ssh.exec_command('openshell sandbox exec my-assistant -- cat /sandbox/.openclaw/openclaw.json 2>&1 | grep allowedOrigins', timeout=15)
out2 = stdout2.read().decode('utf-8', errors='replace')
print(out2)

ssh.close()

