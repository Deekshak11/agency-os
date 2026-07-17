# Automation Targets - Week 1

## Priority 1: Modal Deployment Automation

**Current:** Manual `modal deploy` + verification + cost check
**Target:** One command deploys + verifies + audits

```python
# scripts/deploy_to_modal.py
import subprocess
import sys

def deploy_modal_app(app_file, app_name):
    """One-command Modal deployment with built-in verification"""
    
    print(f"🚀 Deploying {app_name}...")
    
    # Pre-deployment audit
    print("1. Pre-deployment audit...")
    audit_result = subprocess.run(
        ["python", "scripts/cost_audit.py", app_file],
        capture_output=True
    )
    
    if "schedule=" in str(audit_result.stdout):
        print("⚠️ WARNING: Scheduled function detected!")
        response = input("Continue? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Deploy
    print("2. Deploying to Modal...")
    deploy_result = subprocess.run(
        ["modal", "deploy", app_file],
        capture_output=True
    )
    
    if deploy_result.returncode != 0:
        print(f"❌ Deployment failed: {deploy_result.stderr}")
        sys.exit(1)
    
    # Post-deployment verification
    print("3. Verifying deployment...")
    subprocess.run(["modal", "app", "list"])
    
    print(f"✅ {app_name} deployed successfully!")
    print("\n📊 Next steps:")
    print("- Set up billing alerts")
    print("- Test one execution")
    print("- Monitor for 1 hour")

if __name__ == "__main__":
    # Usage: python scripts/deploy_to_modal.py modal_reply_webhook.py reply-triage
    deploy_modal_app(sys.argv[1], sys.argv[2])
```

**Time saved:** 10 mins per deployment → 30 seconds

---

## Priority 2: Cost Audit Automation

**Current:** Manual search for `schedule=`, check Modal dashboard
**Target:** Automated daily audit with alerts

```python
# scripts/cost_audit.py
import os
import re
import subprocess
from datetime import datetime

def audit_codebase():
    """Search for cost triggers in codebase"""
    triggers = []
    
    # Search for scheduled functions
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Check for schedules
                    if 'schedule=' in content or 'cron=' in content:
                        triggers.append({
                            'file': filepath,
                            'type': 'scheduled',
                            'line': content.count('\n', 0, content.find('schedule=')) + 1
                        })
                    
                    # Check for always-on
                    if 'while True' in content:
                        triggers.append({
                            'file': filepath,
                            'type': 'infinite_loop',
                            'line': content.count('\n', 0, content.find('while True')) + 1
                        })
    
    return triggers

def audit_modal_apps():
    """Check deployed Modal apps"""
    result = subprocess.run(['modal', 'app', 'list'], capture_output=True, text=True)
    apps = []
    
    for line in result.stdout.split('\n'):
        if 'deployed' in line:
            apps.append(line.split('│')[1].strip())
    
    return apps

def main():
    print("💰 COST AUDIT REPORT")
    print("=" * 60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Codebase audit
    triggers = audit_codebase()
    if triggers:
        print("⚠️ COST TRIGGERS FOUND IN CODE:")
        for trigger in triggers:
            print(f"  - {trigger['file']}:{trigger['line']} ({trigger['type']})")
    else:
        print("✅ No cost triggers found in codebase")
    
    print()
    
    # Modal apps audit
    apps = audit_modal_apps()
    if apps:
        print("📊 DEPLOYED MODAL APPS:")
        for app in apps:
            print(f"  - {app}")
    else:
        print("✅ No Modal apps deployed")
    
    print()
    print("=" * 60)
    print("💡 RECOMMENDATIONS:")
    print("1. Review scheduled tasks - can they be webhooks?")
    print("2. Check Modal dashboard for unexpected usage")
    print("3. Set up billing alerts if not already done")

if __name__ == "__main__":
    main()
```

**Usage:** Add to cron: `0 9 * * * python scripts/cost_audit.py`

---

## Priority 3: Test Runner Automation

**Current:** Run each test file manually
**Target:** One command runs all tests with report

```python
# scripts/run_tests.py
import subprocess
import sys
from pathlib import Path

def run_all_tests():
    """Run all test files and generate report"""
    
    test_files = list(Path('.').glob('test_*.py'))
    
    if not test_files:
        print("No test files found")
        return
    
    print(f"🧪 Running {len(test_files)} test files...")
    print("=" * 60)
    
    results = []
    
    for test_file in test_files:
        print(f"\n📝 {test_file.name}")
        result = subprocess.run(
            ['python', str(test_file)],
            capture_output=True,
            text=True
        )
        
        passed = result.returncode == 0
        results.append({
            'file': test_file.name,
            'passed': passed,
            'output': result.stdout
        })
        
        if passed:
            print("  ✅ PASSED")
        else:
            print("  ❌ FAILED")
            print(result.stderr[:500])  # First 500 chars of error
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed_count = sum(1 for r in results if r['passed'])
    total_count = len(results)
    
    print(f"Passed: {passed_count}/{total_count}")
    print(f"Failed: {total_count - passed_count}/{total_count}")
    
    if passed_count == total_count:
        print("\n🎉 ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print("\n❌ SOME TESTS FAILED")
        sys.exit(1)

if __name__ == "__main__":
    run_all_tests()
```

**Usage:** `python scripts/run_tests.py`

---

## Priority 4: Template Generator

**Current:** Copy-paste from previous project
**Target:** Generate from template with prompts

```python
# scripts/create_modal_webhook.py
import sys

def create_modal_webhook(name, description):
    """Generate Modal webhook template"""
    
    template = f'''"""
{description}
"""
import modal
from fastapi import FastAPI, Request
from datetime import datetime
import os

app = modal.App("{name}")

image = modal.Image.debian_slim().pip_install("fastapi", "requests")

@app.function(
    image=image,
    secrets=[modal.Secret.from_name("agency-os")]
)
@modal.asgi_app()
def fastapi_app():
    app_fastapi = FastAPI(title="{name}")
    
    @app_fastapi.get("/")
    async def root():
        return {{
            "status": "active",
            "service": "{name}",
            "timestamp": datetime.utcnow().isoformat()
        }}
    
    @app_fastapi.post("/webhook")
    async def webhook_handler(request: Request):
        payload = await request.json()
        
        # TODO: Add your business logic here
        
        return {{"status": "success", "message": "Webhook received"}}
    
    return app_fastapi
'''
    
    filename = f"modal_{name.replace('-', '_')}.py"
    
    with open(filename, 'w') as f:
        f.write(template)
    
    print(f"✅ Created {filename}")
    print(f"\nNext steps:")
    print(f"1. Add business logic to webhook_handler")
    print(f"2. Deploy: modal deploy {filename}")
    print(f"3. Test: curl <url>/webhook")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/create_modal_webhook.py <name> <description>")
        sys.exit(1)
    
    create_modal_webhook(sys.argv[1], ' '.join(sys.argv[2:]))
```

**Usage:** `python scripts/create_modal_webhook.py my-webhook "My webhook description"`

---

## Priority 5: Documentation Generator

**Current:** Write markdown manually
**Target:** Auto-generate from code comments

```python
# scripts/generate_docs.py
import ast
import os

def extract_docstrings(filepath):
    """Extract docstrings from Python file"""
    with open(filepath, 'r') as f:
        tree = ast.parse(f.read())
    
    docs = []
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            docstring = ast.get_docstring(node)
            if docstring:
                docs.append({
                    'name': node.name,
                    'type': 'function' if isinstance(node, ast.FunctionDef) else 'class',
                    'doc': docstring
                })
    
    return docs

def generate_docs_for_directory(directory):
    """Generate README.md from all Python files in directory"""
    
    markdown = f"# {directory.upper()} Documentation\n\n"
    markdown += "Auto-generated from code docstrings.\n\n"
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                filepath = os.path.join(root, file)
                docs = extract_docstrings(filepath)
                
                if docs:
                    markdown += f"## {file}\n\n"
                    
                    for doc in docs:
                        markdown += f"### `{doc['name']}` ({doc['type']})\n\n"
                        markdown += f"{doc['doc']}\n\n"
                        markdown += "---\n\n"
    
    # Write to README
    readme_path = os.path.join(directory, 'README.md')
    with open(readme_path, 'w') as f:
        f.write(markdown)
    
    print(f"✅ Generated {readme_path}")

if __name__ == "__main__":
    generate_docs_for_directory('execution')
```

**Usage:** `python scripts/generate_docs.py`

---

## Implementation Timeline

**Day 1 (Today):**
- ✅ Create scripts/ directory
- ✅ Implement deploy_to_modal.py
- ✅ Implement cost_audit.py

**Day 2:**
- Implement run_tests.py
- Test all 3 scripts
- Add to daily workflow

**Day 3:**
- Implement create_modal_webhook.py
- Implement generate_docs.py
- Create templates/ directory

**Day 4:**
- Set up cron for cost_audit.py
- Add pre-commit hooks
- Document all scripts

**Day 5 (Friday):**
- Measure time saved
- Identify next automation targets
- Review and iterate

---

## Success Criteria

**Automation coverage:** 80% of repetitive tasks
**Time saved per day:** 1-2 hours
**Error reduction:** 90% fewer manual mistakes
**Deploy time:** <30 seconds (vs 10 minutes)

**ROI:**
- Investment: 8 hours to build all scripts
- Time saved: 10 hours per week
- Break-even: Week 1
- Year 1 savings: 500+ hours
