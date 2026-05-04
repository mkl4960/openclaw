---
name: agentmail
description: Skill for sending, receiving, and managing emails using the agentmail-python SDK.
requires:
  env:
    - AGENTMAIL_API_KEY
  python_packages:
    - agentmail
---

# AgentMail Python Skill

This skill allows the agent to control an email inbox via the AgentMail API.

## Initialization
All functions use the shared `_get_client()` helper, which loads `AGENTMAIL_API_KEY` from the environment and returns an authenticated `AgentMail` instance. Raises `ValueError` if the key is missing.

```python
def _get_client() -> AgentMail:
    load_dotenv('/home/mlau/.openclaw/.env')
    api_key = os.getenv('AGENTMAIL_API_KEY')
    if not api_key:
        raise ValueError("AGENTMAIL_API_KEY not found in .env file.")
    return AgentMail(api_key=api_key)
```

## Functions

### send_email
Send an email to a recipient.
```python
def send_email(to: str, subject: str, body: str):
    client = _get_client()
    inbox = client.inboxes.get(inbox_id='laumiex@agentmail.to')
    return client.inboxes.messages.send(inbox_id=inbox.inbox_id, to=to, subject=subject, text=body)
```

Parameters:
- to (string): recipient email
- subject (string): subject line
- body (string): email content

### get_inbox
List available inboxes.
```python
def get_inbox(limit: int = 5):
    client = _get_client()
    return client.inboxes.list(limit=limit)
```

Parameters:
- limit (integer): number of inboxes to fetch (default: 5)

### get_message
Retrieve recent emails.
```python
def get_message(limit: int = 5):
    client = _get_client()
    return client.inboxes.messages.list(inbox_id='laumiex@agentmail.to', limit=limit)
```

Parameters:
- limit (integer): number of emails to fetch (default: 5)

# Prohibitions
CRITICAL: Do not create a virtual environment.
CRITICAL: Do not run 'pip install'. Assume all dependencies are pre-installed in the system environment.
