# HEARTBEAT.md

## Purpose
This file defines how the agent signals that it is alive during long-running operations.

---

## Heartbeat Rules

1. The agent MUST send a heartbeat update every 5–10 seconds while processing any task longer than 5 seconds.

2. A heartbeat can be one of the following:
   - Discord typing indicator refresh
   - Partial response message (e.g. "Still working...")
   - Log output indicating progress

3. If a task exceeds 15 seconds:
   - The agent MUST send a visible progress update to the user

4. If a task exceeds 60 seconds:
   - The agent MUST:
     - Provide a progress summary
     - Offer to continue or cancel

---

## Failure Detection

1. If no progress or heartbeat is emitted for 20 seconds:
   - The task is considered STALLED

2. On stall:
   - Attempt to safely cancel the task
   - Notify the user:
     "Task appears stuck. Restarting or retrying..."

3. If retry fails:
   - Return partial results (if any)
   - Log full error details

---

## Tool Execution Rules

1. All tool calls MUST:
   - Have a timeout (recommended: 30–120 seconds)
   - Emit heartbeat updates while running

2. Long-running tools (scripts, API calls):
   - Must stream output if possible
   - Must not block without feedback

---

## Discord Behavior

1. The agent MUST:
   - Refresh typing indicator every ~5 seconds during processing

2. The agent SHOULD:
   - Stream responses instead of waiting for full completion

3. If response is delayed:
   - Send interim message:
     "Working on it... this may take a bit."

---

## Logging

1. Every task MUST log:
   - Start time
   - Current step
   - Last successful action

2. Logs should update at least every 10 seconds during long tasks

---

## Recovery

1. If agent becomes unresponsive:
   - Restart the task loop (if safe)
   - Do NOT silently fail

2. Always prefer:
   - Partial result + explanation
   over
   - No response

---

## Goal

The user should NEVER be left wondering:
"Did it crash or is it still working?"

The system must always provide visible proof of life.
