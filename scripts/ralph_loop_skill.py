#!/usr/bin/env python3
import os
import sys

# Configuration
PRD_FILE = "PRD.md"
PROGRESS_FILE = "progress.txt"

def read_file(filepath):
    """Reads a file safely, returning None if missing."""
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def get_next_task(prd_content):
    """Parses PRD.md to find the first unchecked task."""
    lines = prd_content.splitlines()
    for i, line in enumerate(lines):
        # Look for unchecked box "- [ ]"
        if line.strip().startswith("- [ ]"):
            return line.strip()[5:].strip() # Remove "- [ ] "
    return None

def get_recent_progress(progress_content, lines=20):
    """Gets the last N lines of progress for context."""
    if not progress_content:
        return "No progress logged yet."
    return "\n".join(progress_content.splitlines()[-lines:])

def generate_prompt():
    """Main logic to build the agent prompt."""
    
    # 1. Read PRD
    prd_content = read_file(PRD_FILE)
    if not prd_content:
        print(f"ERROR: {PRD_FILE} not found. Please create it first.")
        sys.exit(1)

    # 2. Find Task
    next_task = get_next_task(prd_content)
    if not next_task:
        print("🎉 ALL TASKS COMPLETE! The 'Ralph Loop' is finished.")
        sys.exit(0)

    # 3. Read Context
    progress_content = read_file(PROGRESS_FILE)
    recent_progress = get_recent_progress(progress_content)

    # 4. Construct Prompt
    # This is the "Manager" speaking to the "Agent" (Antigravity)
    prompt = f"""
# 🤖 Ralph Loop Instruction (Ralph Wiggum Methodology)
**Your Role**: You are Antigravity, the autonomous engineer.
**Current Mode**: EXECUTION (Fast)

## 🎯 OBJECTIVE: {next_task}

## 📜 RECENT CONTEXT (from {PROGRESS_FILE})
{recent_progress}

## ⚡ YOUR ORDERS (Strict Protocol)
1.  **PLAN**: briefly plan your change (1-2 lines).
2.  **CODE**: Implement the necessary changes for "{next_task}".
3.  **VERIFY**:
    -   If tests exist, run them.
    -   If not, run a **Dry Run** of your script or perform a valid sanity check.
    -   *CRITICAL*: Do not proceed if verification fails. Fix it first.
4.  **DOCUMENT**: Append your result/learnings to `{PROGRESS_FILE}`.
5.  **FINALIZE**:
    -   Mark the task as done (`[x]`) in `{PRD_FILE}`.
    -   **COMMIT**: `git add .` and `git commit -m "feat: {next_task}"` (Required).
6.  **LOOP**: Run `python scripts/ralph_loop_skill.py` again to fetch the next task.
"""
    print(prompt)

if __name__ == "__main__":
    generate_prompt()
