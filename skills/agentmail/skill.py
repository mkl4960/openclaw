#!/home/mlau/.openclaw/workspace/venv/bin/python
import os
from dotenv import load_dotenv
from agentmail import AgentMail

def _get_client() -> AgentMail:
    load_dotenv('/home/mlau/.openclaw/.env')
    api_key = os.getenv('AGENTMAIL_API_KEY')
    if not api_key:
        raise ValueError("AGENTMAIL_API_KEY not found in .env file.")
    return AgentMail(api_key=api_key)

def send_email(to: str, subject: str, body: str):
    client = _get_client()
    inbox = client.inboxes.get(inbox_id='laumiex@agentmail.to')
    inbox_id = inbox.inbox_id
    
    # Add your email sending logic here
    # Example: client.inboxes.send_message(...)
    return client.inboxes.messages.send(inbox_id=inbox_id, to=to, subject=subject, text=body)

def get_inbox(limit: int = 5):
    client = _get_client()
    inbox = client.inboxes.list(limit=limit)
    return inbox

def get_message(limit: int = 5):
    client = _get_client()
    messages = client.inboxes.messages.list(inbox_id='laumiex@agentmail.to', limit=limit)
    return messages
