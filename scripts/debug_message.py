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

def debug_message():
    client = _get_client()
    response = client.inboxes.messages.list(inbox_id='laumiex@agentmail.to', limit=5)
    
    # Extract messages from the response tuple
    messages = next((item[1] for item in response if item[0] == 'messages'), [])
    
    for message in messages:
        if "新澤西州宣恩堂中文主日崇拜連結" in message.subject:
            full_message = client.inboxes.messages.get(inbox_id='laumiex@agentmail.to', message_id=message.message_id)
            print(f"=== Subject: {message.subject} ===")
            print(f"Preview: {full_message.preview}")
            print(f"Headers: {json.dumps({k: str(v) for k, v in full_message.headers.items()}, indent=2) if full_message.headers else 'None'}")
            print(f"Attachments: {len(full_message.attachments) if full_message.attachments else 0}")
            print("=== End of Message ===\n")
            break

if __name__ == "__main__":
    debug_message()