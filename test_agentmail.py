#!/usr/bin/env python3
import os
from pathlib import Path
from dotenv import load_dotenv

_env_path = Path.home() / '.openclaw' / '.env'
if _env_path.exists():
    load_dotenv(dotenv_path=str(_env_path))

api_key = os.getenv('AGENTMAIL_API_KEY')
print(f"API Key: {api_key}")

from agentmail import AgentMail

client = AgentMail(api_key=api_key)
try:
    response = client.inboxes.messages.list(inbox_id="laumiex@agentmail.to", limit=5)
    print(f"Response: {response}")
    print(f"Messages: {len(response.messages)}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()