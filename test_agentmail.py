#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

_env_path = Path.home() / '.openclaw' / '.env'
if _env_path.exists():
    load_dotenv(dotenv_path=str(_env_path))

api_key = os.getenv('AGENTMAIL_API_KEY')
if not api_key:
    print("AGENTMAIL_API_KEY not set")
    sys.exit(1)

from agentmail import AgentMail

client = AgentMail(api_key=api_key)
try:
    inbox_id = "laumiex@agentmail.to"
    response = client.inboxes.messages.list(inbox_id=inbox_id, limit=5)
    print(f"Success: {len(response.messages) if response.messages else 0} messages")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)