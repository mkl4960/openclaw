#!/usr/bin/env python3
import os
import json
from dotenv import load_dotenv
from agentmail import AgentMail

def _get_client():
    load_dotenv('/home/mlau/.openclaw/.env')
    api_key = os.getenv('AGENTMAIL_API_KEY')
    if not api_key:
        raise ValueError("AGENTMAIL_API_KEY not found in .env file.")
    return AgentMail(api_key=api_key)

def debug_emails():
    client = _get_client()
    messages = client.inboxes.messages.list(inbox_id='laumiex@agentmail.to', limit=5)
    print("Message structure:")
    for idx, message in enumerate(messages):
        print(f"Message {idx + 1}: {message}")
        print(f"Type: {type(message)}")

if __name__ == "__main__":
    debug_emails()