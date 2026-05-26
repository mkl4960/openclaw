#!/usr/bin/env python3
"""
Simple test script to check agentmail module and API key
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
_env_path = Path('/home/mlau/.openclaw/.env')
if _env_path.exists():
    load_dotenv(dotenv_path=str(_env_path))
    print("✅ .env file loaded successfully")
else:
    print("❌ .env file not found")

# Check if API key is set
api_key = os.getenv('AGENTMAIL_API_KEY')
if api_key:
    print(f"✅ AGENTMAIL_API_KEY found: {api_key[:20]}...")
else:
    print("❌ AGENTMAIL_API_KEY not found")

# Try to import agentmail
try:
    from agentmail import AgentMail
    print("✅ agentmail module imported successfully")
    
    # Try to create client
    client = AgentMail(api_key=api_key)
    print("✅ AgentMail client created successfully")
    
    # Try to list inboxes
    try:
        response = client.inboxes.list()
        print(f"✅ Listed inboxes successfully: {len(response.inboxes)} inboxes found")
        for inbox in response.inboxes:
            print(f"  - {getattr(inbox, 'email', 'NO_EMAIL')}: {getattr(inbox, 'id', 'NO_ID')}")
    except Exception as e:
        print(f"❌ Failed to list inboxes: {e}")
        
except ImportError as e:
    print(f"❌ Failed to import agentmail: {e}")
except Exception as e:
    print(f"❌ Failed to create AgentMail client: {e}")