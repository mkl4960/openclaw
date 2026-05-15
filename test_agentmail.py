#!/usr/bin/env python3
"""
Test script to check AgentMail API connection
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
_env_path = Path.home() / '.openclaw' / '.env'
if _env_path.exists():
    load_dotenv(dotenv_path=str(_env_path))

from agentmail import AgentMail

# Get API key
api_key = os.getenv('AGENTMAIL_API_KEY')
if not api_key:
    print("ERROR: AGENTMAIL_API_KEY not set")
    exit(1)

print(f"API Key: {api_key[:20]}...")

try:
    # Create client
    client = AgentMail(api_key=api_key)
    print("✅ AgentMail client created successfully")
    
    # Try to list inboxes
    response = client.inboxes.list()
    print(f"✅ Inboxes listed successfully: {response}")
    
    # Try to get messages from the specific inbox
    response = client.inboxes.messages.list(
        inbox_id="laumiex@agentmail.to",
        limit=5
    )
    print(f"✅ Messages listed successfully: {response}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()