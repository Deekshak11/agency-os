---
name: Ralph Loop
description: The autonomous execution loop for Antigravity.
---

# Ralph Loop Skill

## ❓ What is it?
The **Ralph Loop** is your "Autopilot Mode". It uses a Python script to manage your task list so you don't get lost or hallucinate.

## 👤 Who is the Agent?
**YOU** are the agent. The script (`scripts/ralph_loop_skill.py`) is your **Manager**. It tells you what to do.

## 🚀 Ralph Wiggum Protocol (Strict)
When you run `python scripts/ralph_loop_skill.py`, you are entering the **Wiggum Loop**. You must follow these steps for **EVERY** iteration:

1.  **Read the Orders**: The script serves as your Manager. It defines the *single* next task.
2.  **Plan**: Think briefly.
3.  **Code**: Implement the task.
4.  **Verify (CRITICAL)**:
    -   Run tests if available.
    -   Run dry-runs or sanity checks.
    -   **NEVER** commit broken code.
5.  **Commit**:
    -   `git add .`
    -   `git commit -m "feat: [Task Name]"`
6.  **Document**: Append result to `progress.txt`.
7.  **Loop**: Run the script again immediately.

## ✅ Success Criteria
- **Green Tests**: Code must be verified before committing.
- **Git History**: Every task has a corresponding commit.
- **Fresh Context**: The loop relies on `progress.txt` and `PRD.md` state, not conversation history.

## 🛠 Dependencies
- `PRD.md` (The Task List - Must exist in root)
- `progress.txt` (The Log - Created automatically if missing)
