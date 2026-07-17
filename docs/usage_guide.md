# How to Drive the "Fence" System

## 1. Mid-Chat Updates: "Make it Automatic"
**Q: Do I prompt it to remember choices or does it do it automatically?**
**A:** With the new Spec-Driven flow, it works like this:

- **Implicit Updates**: For minor things, the agent *should* update `active_task.md` automatically.
- **Explicit Updates (The Fence)**: If you make a **Decision** (e.g., "Change the target to 500 leads"), the agent **CANNOT** proceed until it updates `decisions.md` and the Spec.
- **Why?** The "Blindspot Check" requires checking the Spec. If the Spec is stale, the check fails. **Updates are forced by the process.**

## 2. Context Awareness
**Q: How do I know if the model is getting "dumb" (full context)?**
**A:** Technical limitation: I cannot see my own token count in real-time.
**The Fix**: A heuristic rule in `personality.md`.
- **Rule**: *"If the conversation exceeds 20 turns, propose a 'Context Refresh': Summarize conversation to `active_task.md` and ask user to restart session."*

## 3. Ending the Session
**Q: What do I prompt?**
**A:** Just type: **"Session End."**

**Q: What happens exactly?**
The agent executes the **Session Shutdown Protocol** (hard-coded in `personality.md`):
1.  **Diff Check**: Compares start-of-session `strategic.md` vs. now.
2.  **State Dump**: Writes all pending volatile thoughts to `active_task.md`.
3.  **Git Sync**: Commits changes.

**Q: How do I verify integrity?**
The agent MUST output a **Session Integrity Report**:
```markdown
## Session Integrity Report
✅ Learnings Captured: 2 new items added to strategic.md
✅ Decisions Logged: 1 pivot recorded in decisions.md
✅ Next State: active_task.md updated for next session
❌ WARNING: spec/email_flow.md looks stale based on recent chat.
```
**You verify by looking for green checks.** If you see a warning or a missing check, you know it missed something.
