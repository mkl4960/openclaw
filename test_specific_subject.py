#!/usr/bin/env python3
"""
Test script to check if we can find messages with specific subject
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
            email = getattr(inbox, 'email', 'NO_EMAIL')
            inbox_id = getattr(inbox, 'id', None) or getattr(inbox, 'inbox_id', None)
            print(f"  - Email: {email}")
            print(f"  - Inbox ID: {inbox_id}")
            
            # Try to get messages from this inbox
            if inbox_id:
                try:
                    # Look for messages with our target subject
                    target_subject = "新澤西州宣恩堂中文主日崇拜連結"
                    messages_response = client.inboxes.messages.list(inbox_id=inbox_id, limit=50)
                    messages = messages_response.messages or []
                    print(f"  ✅ Retrieved {len(messages)} messages from inbox {inbox_id}")
                    
                    # Process each message
                    matching_messages = []
                    for msg in messages:
                        msg_id = getattr(msg, 'message_id', 'NO_ID')
                        subject = getattr(msg, 'subject', 'NO_SUBJECT')
                        print(f"    - Message ID: {msg_id}")
                        print(f"    - Subject: {subject}")
                        
                        if target_subject in str(subject):
                            matching_messages.append(msg)
                            print(f"    ✅ MATCHING MESSAGE FOUND!")
                    
                    if matching_messages:
                        print(f"  🎯 Found {len(matching_messages)} message(s) with target subject")
                    else:
                        print(f"  ❌ No messages found with target subject")
                        
                except Exception as e:
                    print(f"  ❌ Failed to get messages from inbox {inbox_id}: {e}")
            else:
                print(f"  ❌ No inbox ID found for email {email}")
                
    except Exception as e:
        print(f"❌ Failed to list inboxes: {e}")
        
except ImportError as e:
    print(f"❌ Failed to import agentmail: {e}")
except Exception as e:
    print(f"❌ Failed to create AgentMail client: {e}")